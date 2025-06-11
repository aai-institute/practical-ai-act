from typing import Protocol

import pandas as pd

class ProbabilisticPredictor(Protocol):
    def predict(self, X, **params) -> pd.Series: ...
    def predict_proba(self, X, **params) -> pd.Series: ...


def build_reference_data(
    model: ProbabilisticPredictor,
    X: pd.DataFrame,
    y_true: pd.DataFrame,
) -> pd.DataFrame:
    reference_df = pd.DataFrame(X)
    reference_df["target"] = y_true
    reference_df["prediction"] = model.predict(X)
    reference_df["prediction_probability"] = model.predict_proba(X)[:, 1]

    return reference_df
