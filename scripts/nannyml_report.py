"""Create an Evidently report from the logged predictions in an SQLite3 database."""

import json
import sqlite3
from pathlib import Path

import mlflow
import mlflow.models
import pandas as pd


def fetch_test_data(model_uri: str) -> pd.DataFrame:
    """Fetch the test data for the given model from MLflow."""

    model = mlflow.models.get_model_info(model_uri)
    if model is None:
        raise ValueError(f"Model not found: {model_uri}")

    run = mlflow.get_run(model.run_id)
    if run is None:
        raise ValueError(f"Run not found: {model.run_id}")

    client = mlflow.client.MlflowClient()
    dataset = next(
        (
            a.path
            for a in client.list_artifacts(run.info.run_id)
            if a.path.endswith("reference.parquet")
        ),
        None,
    )
    if dataset is None:
        raise ValueError(f"MLflow artifact not found: {run.info.run_id}")

    local_path = client.download_artifacts(run.info.run_id, dataset)
    df = pd.read_parquet(local_path)
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
            proba = output_data["probabilities"][0]
        else:
            # Simple argmax predictions
            prediction_data = int(output_data)
            proba = []
        records.append(input_data + [prediction_data, proba])

    return pd.DataFrame.from_records(records, columns=columns)


def expand_predict_proba(
    df: pd.DataFrame, col: str = "prediction_probability"
) -> pd.DataFrame:
    pred_proba_expanded = pd.DataFrame(
        df[col].tolist(),
        columns=[f"prob_{idx}" for idx in range(3)],
        index=df.index,
    )
    df = pd.concat(
        [df.drop(col, axis="columns"), pred_proba_expanded],
        axis=1,
    )
    return df


PREDICTIONS_DB_FILE = Path("predictions.sqlite3")
PREDICTIONS_TABLE = "predictions"

mlflow.set_tracking_uri("http://localhost:5000")

db = sqlite3.connect(PREDICTIONS_DB_FILE)

model_versions = [
    row[0]
    for row in db.execute(
        f'SELECT DISTINCT metadata->>"model_version" from {PREDICTIONS_TABLE}'
    ).fetchall()
]
assert len(model_versions) == 1, "Multiple model versions found in the database"

print(f"Fetching test data for model {model_versions[0]}")
reference_df = fetch_test_data(model_versions[0])

predictions = db.execute(f"SELECT input, output from {PREDICTIONS_TABLE}").fetchall()
analysis_df = predictions_to_dataset(
    predictions,
    columns=list(reference_df.columns)[:4] + ["prediction", "prediction_probability"],
)

analysis_df = expand_predict_proba(analysis_df)
reference_df = expand_predict_proba(reference_df)

print("Analysis:", analysis_df.columns)
print("Reference:", reference_df.columns)


# NannyML reporting
import nannyml as nml

chunk_size = 100
estimator = nml.CBPE(
    problem_type="classification_multiclass",
    y_pred_proba={idx: f"prob_{idx}" for idx in range(3)},
    y_pred="prediction",
    y_true="target",
    metrics=["roc_auc", "f1"],
    chunk_size=chunk_size,
)
estimator.fit(reference_df)
estimated_performance = estimator.estimate(analysis_df)

fig = estimated_performance.plot()
fig.show()
