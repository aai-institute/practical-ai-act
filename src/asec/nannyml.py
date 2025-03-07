from typing import Protocol

import pandas as pd
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


