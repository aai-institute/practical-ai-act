import os

import pandas as pd
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pickle

from mlserver.codecs import NumpyCodec

app = FastAPI()
estimator_path = os.getenv("NANNYML_ESTIMATOR")
with open(estimator_path, "rb") as f:
    estimator = pickle.load(f)


def load_predictions(cursor: psycopg2.extensions.cursor) -> pd.DataFrame:

    query ="""
        SELECT
            req.raw_request as request,
            resp.raw_response as response
        FROM inference_requests req INNER JOIN inference_responses resp
        ON (req.id = resp.id)
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    from mlserver.codecs import PandasCodec
    from mlserver.types import InferenceRequest, InferenceResponse

    results = []
    for row in rows:
        req = InferenceRequest.model_validate(row["request"])
        resp = InferenceResponse.model_validate(row["response"])
        req_df = PandasCodec.decode_request(req)

        outputs = {o.name: NumpyCodec.decode_output(o) for o in resp.outputs}
        prediction = pd.Series(outputs["predict"].ravel(), name="prediction")
        prediction_probability = pd.DataFrame(
            outputs["predict_proba"].tolist(),
            columns=[f"prob_{i}" for i in range(outputs["predict_proba"].shape[1])],
        )

        df = req_df.copy()
        df = pd.concat([df, prediction, prediction_probability], axis=1)
        results.append(df)

    return pd.concat(results, axis=0)


def generate_figure():
    db_conn: psycopg2.extensions.connection | None = None
    try:
        db_conn = psycopg2.connect(
            host="postgres",
            user="postgres_user",
            password="postgres_password",
            dbname="hr_assistant",
        )
        with db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            analysis_df = load_predictions(cur)
    finally:
        if db_conn:
            db_conn.close()

    estimated_performance = estimator.estimate(analysis_df)
    fig = estimated_performance.plot()
    return fig.to_html(full_html=False)


@app.get("/", response_class=HTMLResponse)
def index():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://unpkg.com/htmx.org@1.9.4"></script>
    </head>
    <body>
        <div id="graph-container" hx-get="/update_data" hx-trigger="every 2s"></div>
    </body>
    </html>
    """


@app.get("/update_data", response_class=HTMLResponse)
def update_data():
    return generate_figure()

