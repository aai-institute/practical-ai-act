from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata

ALL_FEATURES = (
    CensusASECMetadata.CATEGORICAL_FEATURES
    + CensusASECMetadata.NUMERIC_FEATURES
    + CensusASECMetadata.ORDINAL_FEATURES
)


def build_pipeline(classifier: Any, exclude=None, encode_categoricals=True) -> Pipeline:
    """Constructs a preprocessing and classification pipeline.

    Parameters
    ----------
    classifier : Any
        Classifier to use in the pipeline.

    Returns
    -------
    Pipeline
        A scikit-learn pipeline with preprocessing and classifications steps.
    """

    categorical_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])
    numerical_pipeline = Pipeline([("scaler", StandardScaler())])
    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    column_transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                categorical_pipeline if encode_categoricals else "passthrough",
                CensusASECMetadata.CATEGORICAL_FEATURES,
            ),
            (
                "numerical_pipeline",
                numerical_pipeline,
                [feat for feat in CensusASECMetadata.NUMERIC_FEATURES if not feat in exclude] if exclude is not None else CensusASECMetadata.NUMERIC_FEATURES,
            ),
            (
                "ordinal_pipeline",
                ordinal_pipeline,
                CensusASECMetadata.ORDINAL_FEATURES,
            ),
        ]
    )

    return Pipeline(
        [
            ("preprocessor", column_transformer),
            ("classifier", classifier),
        ]
    )


def train_income_prediction_model(classifier: Any, train_data: pd.DataFrame) -> Pipeline:
    """Trains an income prediction model using a given classifier.

    Parameters
    ----------
    classifier : Any
        Scikit-learn compatible classifier.
    train_data : pd.DataFrame
        Training dataset.

    Returns
    -------
    Pipeline
        Trained scikit-learn pipeline.
    """
    train_input = train_data[ALL_FEATURES]
    train_output = train_data[CensusASECMetadata.TARGET]

    pipeline = build_pipeline(classifier)
    pipeline.fit(train_input, train_output)

    return pipeline


def train_income_prediction_xgboost_classifier(
    train_data: pd.DataFrame, random_state: int = 42
) -> Pipeline:
    """Trains an XGBoost classifier for income prediction.

    Parameters
    ----------
    train_data : pd.DataFrame
        Training dataset.
    random_state : int, default is 42
        Random seed for model reproducibility.

    Returns
    -------
    Pipeline
        Trained pipeline with an XGBoost classifier.
    """
    classifier = XGBClassifier(random_state=random_state)
    return train_income_prediction_model(classifier, train_data)
