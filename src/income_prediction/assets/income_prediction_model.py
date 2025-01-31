import mlflow
import pandas as pd
from dagster import AssetExecutionContext, asset
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.resources.configuration import Config
from income_prediction.resources.mlflow_session import MlflowSession

ALL_FEATURES = list(
    CensusASECMetadata.CATEGORICAL_FEATURES
    + CensusASECMetadata.NUMERIC_FEATURES
    + CensusASECMetadata.ORDINAL_FEATURES
)


@asset
def income_prediction_model(
    context: AssetExecutionContext,
    config: Config,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> None:
    """Trains and evaluates an income prediction model using an XGBoost classifier.

    Experiment metrics and artifacts are logged to MLflow.

    Parameters
    ----------
    context : AssetExecutionContext
        Dagster execution context.
    config : Config
        Pipeline configuration settings.
    mlflow_session : MlflowSession
        MLflow session manager for experiment tracking.
    train_data : pd.DataFrame
        Training dataset containing features and target values.
    test_data: pd.DataFrame
        Test dataset for model evaluation.

    Returns
    -------
    None
        Saves model artifacts to MLflow.
    """

    train_input = train_data[ALL_FEATURES]
    train_output = train_data[CensusASECMetadata.TARGET]

    categorical_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])

    numerical_pipeline = Pipeline([("scaler", StandardScaler())])

    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    column_transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                categorical_pipeline,
                CensusASECMetadata.CATEGORICAL_FEATURES,
            ),
            (
                "numerical_pipeline",
                numerical_pipeline,
                CensusASECMetadata.NUMERIC_FEATURES,
            ),
            (
                "ordinal_pipeline",
                ordinal_pipeline,
                CensusASECMetadata.ORDINAL_FEATURES,
            ),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessor", column_transformer),
            ("classifier", XGBClassifier(random_state=config.random_state)),
        ]
    )

    with mlflow_session.get_run(context):
        mlflow.sklearn.autolog()
        mlflow.xgboost.autolog()

        pipeline.fit(train_input, train_output)

        mlflow.evaluate(
            model=pipeline.predict,
            data=test_data,
            targets=CensusASECMetadata.TARGET,
            model_type="classifier",
        )
