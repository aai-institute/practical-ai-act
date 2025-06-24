import logging
import os
import pickle
from datetime import datetime

import pandas as pd
import psycopg2
import psycopg2.extensions
import psycopg2.extras
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.types import InferenceRequest, InferenceResponse
from pytz import utc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
estimator_path = os.getenv("NANNYML_ESTIMATOR")
with open(estimator_path, "rb") as f:
    estimator = pickle.load(f)


postgres_config = {
    "host": "postgres",
    "user": "postgres_user",
    "password": "postgres_password",
    "dbname": "hr_assistant",
}

_predictions: pd.DataFrame | None = None
_last_timestamp: datetime | None = None


def build_query() -> str:
    global _last_timestamp

    query = """
        SELECT
            req.raw_request as request,
            resp.raw_response as response
        FROM inference_requests req INNER JOIN inference_responses resp
        ON (req.id = resp.id)
    """

    if _last_timestamp:
        query += (
            f"WHERE req.timestamp > '{_last_timestamp.astimezone(utc).isoformat()}'"
        )
    _last_timestamp = datetime.now()

    return query


def process_prediction_row(row: dict) -> pd.DataFrame:
    """Process a single row from the database into a DataFrame."""
    try:
        req = InferenceRequest.model_validate(row["request"])
        resp = InferenceResponse.model_validate(row["response"])

        # Decode request data
        req_df = PandasCodec.decode_request(req)

        # Extract predictions
        outputs = {o.name: NumpyCodec.decode_output(o) for o in resp.outputs}

        if "predict" not in outputs or "predict_proba" not in outputs:
            logger.warning("Missing required outputs in response")
            return pd.DataFrame()

        prediction = pd.Series(outputs["predict"].ravel(), name="prediction")
        prediction_probability = pd.Series(
            outputs["predict_proba"][:, 1], name="prediction_probability"
        )

        # Combine data
        df = req_df.copy()
        df = pd.concat([df, prediction, prediction_probability], axis=1)

        return df
    except Exception as e:
        logger.error(f"Error processing prediction row: {e}")
        return pd.DataFrame()


def load_predictions(cursor: psycopg2.extensions.cursor) -> pd.DataFrame:
    global _predictions

    query = build_query()
    cursor.execute(query)
    rows = cursor.fetchall()

    results = []
    for row in rows:
        df = process_prediction_row(row)
        if not df.empty:
            results.append(df)

    if not results:
        logger.info("No new predictions found.")
        return _predictions if _predictions is not None else pd.DataFrame()

    new_predictions = pd.concat(results, axis=0)
    logger.info(f"Loaded {len(new_predictions)} new predictions")

    if _predictions is not None:
        _predictions = pd.concat([_predictions, new_predictions], axis=0)
    else:
        _predictions = new_predictions

    return _predictions


def generate_figure():
    db_conn: psycopg2.extensions.connection | None = None
    try:
        db_conn = psycopg2.connect(**postgres_config)
        with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            analysis_df = load_predictions(cur)
    finally:
        if db_conn:
            db_conn.close()

    if analysis_df.empty:
        logger.warning("No data available for analysis.")
        return "<p>No data available for analysis.</p>"

    estimated_performance = estimator.estimate(analysis_df)
    fig = estimated_performance.plot()
    return fig.to_html(full_html=False)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NannyML Monitoring Dashboard</title>
        <script src="https://unpkg.com/htmx.org@2.0.4"></script>
        <style>
            body { display: flex; align-items: center; justify-content: center; height: 100vh; }
            #graph-container { width: 90vw; }
            .loading { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <div id="graph-container"
             hx-get="/update_data"
             hx-trigger="every 5s"
             hx-indicator="#loading">
            <div class="loading">Loading initial data...</div>
        </div>
        <div id="loading" class="loading" style="display: none;">Updating...</div>
    </body>
    </html>
    """


@app.get("/update_data", response_class=HTMLResponse)
def update_data():
    return generate_figure()
