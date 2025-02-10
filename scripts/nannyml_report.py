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
            if a.path.endswith("reference_data.parquet")
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
        input_data = json.loads(row[0])[0]

        output_data = json.loads(row[1])
        if isinstance(output_data, dict):
            # Predictions with probabilities
            prediction_data = output_data["class"][0]
            proba = output_data["probabilities"][0]
        else:
            # Simple argmax predictions
            prediction_data = int(output_data)
            proba = []
        records.append(input_data | {"prediction": prediction_data, "prediction_probability": proba})

    return pd.DataFrame.from_records(records, columns=columns)


def expand_predict_proba(
    df: pd.DataFrame, col: str = "prediction_probability"
) -> pd.DataFrame:
    pred_proba_expanded = pd.DataFrame(
        df[col].tolist(),
        columns=[f"prob_{idx}" for idx in range(NUM_CLASSES)],
        index=df.index,
    )
    df = pd.concat(
        [df.drop(col, axis="columns"), pred_proba_expanded],
        axis=1,
    )
    return df


PREDICTIONS_DB_FILE = Path(__file__).parents[1] / "predictions.sqlite3"
PREDICTIONS_TABLE = "predictions"
NUM_CLASSES = 2

mlflow.set_tracking_uri("/Users/kristof/Projects/twai-pipeline/compliance_journey/step01_logging/mlruns"
                            )

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
    columns=list(reference_df.drop("target", axis=1).columns),
)

reference_df["prediction_probability"] = reference_df["prediction_probability"].map(lambda arr: [float(v) for v in arr])

analysis_df = expand_predict_proba(analysis_df)
reference_df = expand_predict_proba(reference_df)

print("Analysis:", analysis_df.columns)
print("Reference:", reference_df.columns)


# NannyML reporting
import nannyml as nml

CLASSES = ["<=50K", ">50K"]
label_map = {cls: idx for idx, cls in enumerate(CLASSES)}

reference_df["prediction"] = reference_df["prediction"].map(label_map)
reference_df["target"] = reference_df["target"].map(label_map)

analysis_df["prediction"] = analysis_df["prediction"].map(label_map)

chunk_size = 500
estimator = nml.CBPE(
    problem_type="classification_binary",
    y_pred_proba="prob_1",
    y_pred="prediction",
    y_true="target",
    metrics=["roc_auc", "f1"],
    chunk_size=chunk_size,
)
estimator.fit(reference_df)
estimated_performance = estimator.estimate(analysis_df)

fig = estimated_performance.plot()
fig.show()
