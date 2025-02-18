import dagster as dg
import mlflow
import pandas as pd
import sklearn.pipeline
from sklearn.model_selection import train_test_split

from income_prediction.assets.census_asec_dataset import download_and_filter_census_data
from income_prediction.assets.income_prediction_features import (
    get_income_prediction_features,
)
from income_prediction.assets.income_prediction_model import (
    train_income_prediction_xgboost_classifier,
)
from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.resources.configuration import Config
from income_prediction.resources.mlflow_session import MlflowSession


@dg.asset(io_manager_key="csv_io_manager")
def census_asec_dataset(config: Config):
    """Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria."""
    return download_and_filter_census_data(config.census_asec_dataset_year)


@dg.asset(io_manager_key="csv_io_manager")
def income_prediction_features(
    config: Config, census_asec_dataset: pd.DataFrame
) -> pd.DataFrame:
    """Pre-processes the Census ASEC dataset for income prediction."""
    return get_income_prediction_features(config.salary_bands, census_asec_dataset)


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="csv_io_manager"),
        "test_data": dg.AssetOut(io_manager_key="csv_io_manager"),
    }
)
def train_test_data(
    config: Config, income_prediction_features: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        income_prediction_features, random_state=config.random_state
    )
    return train_data, test_data


@dg.asset()
def income_prediction_model_xgboost(
    context: dg.AssetExecutionContext,
    config: Config,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> sklearn.pipeline.Pipeline:
    """Trains and evaluates the income prediction classifier with XGBoostClassifier."""

    model_name = "xgboost-classifier"
    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name=model_name):
            mlflow.autolog(log_datasets=False)

            pipeline = train_income_prediction_xgboost_classifier(
                train_data, config.random_state
            )

            mlflow.register_model(
                name=model_name,
                model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
            )
            mlflow.evaluate(
                model=pipeline.predict,
                data=test_data,
                targets=CensusASECMetadata.TARGET,
                model_type="classifier",
            )

    return pipeline


@dg.asset(io_manager_key="csv_io_manager")
def reference_dataset(
    income_prediction_model_xgboost: sklearn.pipeline.Pipeline,
    test_data: pd.DataFrame,
) -> pd.DataFrame:
    """Reference dataset for post-deployment performance monitoring

    Based on predictions of the model on the test dataset"""

    y_proba = income_prediction_model_xgboost.predict_proba(test_data)

    df = test_data.rename({CensusASECMetadata.TARGET: "target"}, axis=1)
    df = pd.concat(
        [df, pd.Series(y_proba.tolist(), name="predicted_probabilities")], axis=1
    )
    return df
