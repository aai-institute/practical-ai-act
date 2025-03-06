from typing import Protocol

import pandas as pd
import psycopg2.extensions
from mlserver.codecs import NumpyCodec
from sklearn.preprocessing import LabelEncoder

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
    query = """
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
