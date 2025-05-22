"""Create an Evidently report from the logged predictions in an SQLite3 database."""

import json
import sqlite3
from pathlib import Path

import mlflow
import mlflow.models
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.report import Report
from evidently.ui.workspace import Workspace


def fetch_test_data(model_uri: str) -> pd.DataFrame:
    """Fetch the test data for the given model from MLflow."""

    model = mlflow.models.get_model_info(model_uri)
    if model is None:
        raise ValueError(f"Model not found: {model_uri}")

    run = mlflow.get_run(model.run_id)
    if run is None:
        raise ValueError(f"Run not found: {model.run_id}")

    client = mlflow.client.MlflowClient()
    dataset = next((a.path for a in client.list_artifacts(run.info.run_id) if a.path.endswith("test.parquet")), None)
    if dataset is None:
        raise ValueError(f"MLflow artifact not found: {run.info.run_id}")

    local_path = client.download_artifacts(run.info.run_id, dataset)
    df = pd.read_parquet(local_path)
    print(df.head())
    return df


def predictions_to_dataset(predictions: list, columns: list[str]) -> pd.DataFrame:
    """Convert the logged predictions to a dataset for analysis."""

    records = []
    for row in predictions:
        input_data = json.loads(row[0])

        output_data = json.loads(row[1])
        if isinstance(output_data, dict):
            # Predictions with probabilities
            prediction_data = int(output_data["class"])
        else:
            # Simple argmax predictions
            prediction_data = int(output_data)
        records.append(input_data + [prediction_data])

    return pd.DataFrame.from_records(records, columns=columns)


def create_report(ref_df: pd.DataFrame, df: pd.DataFrame) -> Report:
    data_drift_report = Report(
        metrics=[
            DataQualityPreset(),
            DataDriftPreset(),
        ],
    )

    col_mapping = ColumnMapping(
        target="target",
        numerical_features=list(ref_df.columns),
        prediction="target",
        task="classification",
    )

    data_drift_report.run(
        reference_data=ref_df,
        current_data=df,
        column_mapping=col_mapping,
    )
    return data_drift_report


ws = Workspace.create("evidently")
prj = ws.search_project("hr_assistant")
if not prj:
    prj = ws.create_project("hr_assistant")
else:
    prj = prj[0]


PREDICTIONS_DB_FILE = Path("predictions.sqlite3")
PREDICTIONS_TABLE = "predictions"

mlflow.set_tracking_uri("http://localhost:5000")

db = sqlite3.connect(PREDICTIONS_DB_FILE)

model_versions = [row[0] for row in db.execute(f'SELECT DISTINCT metadata->>"model_version" from {PREDICTIONS_TABLE}').fetchall()]
assert len(model_versions) == 1, "Multiple model versions found in the database"

print(f"Fetching test data for model {model_versions[0]}")
ref_df = fetch_test_data(model_versions[0])

predictions = db.execute(f"SELECT input, output from {PREDICTIONS_TABLE}").fetchall()
report_df = predictions_to_dataset(predictions, columns=ref_df.columns)

report = create_report(ref_df, report_df)
ws.add_report(prj.id, report)
