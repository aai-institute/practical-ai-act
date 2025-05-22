"""Create an Evidently report from the logged predictions in an SQLite3 database."""

import os

import mlflow.models
import nannyml as nml
import psycopg2.extras
from config import FILE_NAME_ASEC
from sensai.util.cache import pickle_cached
from sklearn.model_selection import train_test_split

from asec.data import download_and_filter_census_data
from asec.features import get_income_prediction_features
from asec.nannyml import build_reference_data
from deploy.nannyml.main import load_predictions
from income_prediction.resources.configuration import Config

# Pretend we're in `dagster dev` to force correct environment selection
os.putenv("DAGSTER_IS_DEV_CLI", "1")

db_conn = psycopg2.connect(
    host="localhost",
    user="postgres_user",
    password="postgres_password",
    dbname="hr_assistant",
)

try:
    with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        analysis_df = load_predictions(cur)
finally:
    db_conn.close()

# NannyML reporting

data = pickle_cached(FILE_NAME_ASEC)(download_and_filter_census_data)(year=2024)
data = get_income_prediction_features(Config().salary_bands, data)
X, y = data.drop(columns=["SALARY_BAND"]), data["SALARY_BAND"]

_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=31)

mlflow.set_tracking_uri("http://localhost:50000")
MODEL_URI = "models:/xgboost-classifier/latest"
model = mlflow.sklearn.load_model(MODEL_URI)

reference_df = build_reference_data(
    model, X_test, y_test, encoder=model.steps[-1][1].encoder
)

chunk_size = 250
estimator = nml.CBPE(
    problem_type="classification_multiclass",
    y_pred_proba={
        idx: f"prob_{idx}"
        for idx in range(
            len(Config().salary_bands) + 1
        )  # Account for implicit highest band
    },
    y_pred="prediction",
    y_true="target",
    metrics=["roc_auc"],
    chunk_size=chunk_size,
)
estimator.fit(reference_df)
estimated_performance = estimator.estimate(analysis_df)

fig = estimated_performance.plot()
fig.show()
fig.write_image("nannyml_report.png")
