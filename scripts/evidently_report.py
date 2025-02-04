"""Create an Evidently report from the logged predictions in an SQLite3 database."""

import json
import sqlite3
from pathlib import Path

import pandas as pd
import sklearn.datasets

from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.report import Report
from evidently.ui.workspace import Workspace

iris = sklearn.datasets.load_iris(as_frame=True)
iris_df = iris.frame


def predictions_to_dataset(predictions: list) -> pd.DataFrame:
    """Convert the logged predictions to a dataset for analysis."""

    records = []
    for row in predictions:
        input_data = json.loads(row[0])

        output_data = json.loads(row[1])
        if isinstance(output_data, dict):
            # Predictions with probabilities
            prediction_data = int(["class"])
        else:
            # Simple argmax predictions
            prediction_data = int(output_data)
        records.append(input_data + [prediction_data])

    return pd.DataFrame.from_records(records, columns=iris.feature_names + ["target"])


def create_report(df: pd.DataFrame) -> Report:
    data_drift_report = Report(
        metrics=[
            DataQualityPreset(),
            DataDriftPreset(),
        ],
    )

    col_mapping = ColumnMapping(
        target="target",
        numerical_features=iris.feature_names,
        prediction="target",
        task="classification",
        target_names=dict(enumerate(iris.target_names.tolist())),
    )

    data_drift_report.run(
        reference_data=iris_df,
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
db = sqlite3.connect(PREDICTIONS_DB_FILE)

predictions = db.execute(f"SELECT input, output from {PREDICTIONS_TABLE}").fetchall()
report_df = predictions_to_dataset(predictions)

report = create_report(report_df)
ws.add_report(prj.id, report)
