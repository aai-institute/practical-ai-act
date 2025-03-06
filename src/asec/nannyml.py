import json
from typing import Protocol

import psycopg2.extensions
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator
import pandas as pd
import mlflow
from asec.util import flatten_column


class ProbabilisticPredictor(Protocol):
    def predict(self, X, **params) -> pd.Series: ...
    def predict_proba(self, X, **params) -> pd.Series: ...


def build_reference_data(
    model: ProbabilisticPredictor,
    X: pd.DataFrame,
    y_true: pd.DataFrame,
    encoder: LabelEncoder | None = None,
) -> pd.DataFrame:
    reference_df = pd.DataFrame(X)
    reference_df["target"] = y_true
    reference_df["prediction"] = model.predict(X)
    reference_df["prediction_probability"] = model.predict_proba(X).tolist()
    reference_df = flatten_column(
        reference_df, "prediction_probability", name_prefix="prob"
    )

    if encoder is not None:
        reference_df["prediction"] = encoder.transform(reference_df["prediction"])
        reference_df["target"] = encoder.transform(reference_df["target"])

    return reference_df


def load_predictions(cursor: psycopg2.extensions.cursor) -> pd.DataFrame:
    query = f"""
        SELECT req.id as req_id, req.parameters as req_parameters, req.inputs as req_inputs, req.outputs as req_outputs, resp.id as resp_id, resp.model_name as resp_model_name, resp.model_version as resp_model_version, resp.parameters as resp_parameters, resp.outputs as resp_outputs
        FROM inference_requests req INNER JOIN inference_responses resp
        ON (req.id = resp.id)
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    from mlserver.types import InferenceRequest, InferenceResponse
    from mlserver.codecs import PandasCodec

    results = []
    for row in rows:
        req = InferenceRequest.model_validate({
            k.removeprefix("req_"): v for k, v in row.items() if k.startswith("req_")
        })
        resp = InferenceResponse.model_validate({
            k.removeprefix("resp_"): v for k, v in row.items() if k.startswith("resp_")
        })
        req_df = PandasCodec.decode_request(req)
        resp_df = PandasCodec.decode_response(resp)

        df = req_df.copy()
        df["target"] = resp_df[resp_df.columns[0]]
        results.append(df)

    return pd.concat(results, axis=0)
