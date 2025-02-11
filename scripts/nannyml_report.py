"""Create an Evidently report from the logged predictions in an SQLite3 database."""

import nannyml as nml
from asec.data import AdultData
from config import FILE_NAME_ADULT
from sklearn.model_selection import train_test_split

import sqlite3
from pathlib import Path

import mlflow.models

from asec.nannyml import build_reference_data, load_predictions

PREDICTIONS_DB_FILE = Path(__file__).parents[1] / "predictions.sqlite3"
PREDICTIONS_TABLE = "predictions"

# NannyML reporting

data = AdultData(FILE_NAME_ADULT)
X, y = data.load_input_output_data()
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=31)
MODEL_URI = "models:/xgboost-classifier/latest"
model = mlflow.sklearn.load_model(MODEL_URI)

reference_df = build_reference_data(
    model, X_test, y_test, encoder=model.steps[-1][1].encoder
)
analysis_df = load_predictions(
    sqlite3.connect(PREDICTIONS_DB_FILE),
    PREDICTIONS_TABLE,
    encoder=model.steps[-1][1].encoder,
)


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
