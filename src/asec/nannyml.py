import json
from typing import Protocol
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator
import pandas as pd
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


def load_predictions(
    db, table_name, encoder: LabelEncoder | None = None
) -> pd.DataFrame:
    predictions = db.execute(f"SELECT input, output from {table_name}").fetchall()
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
        records.append(
            input_data
            | {"prediction": prediction_data, "prediction_probability": proba}
        )

    df = pd.DataFrame.from_records(records)
    df = flatten_column(df, "prediction_probability", name_prefix="prob")

    if encoder is not None:
        df["prediction"] = encoder.transform(df["prediction"])

    return df
