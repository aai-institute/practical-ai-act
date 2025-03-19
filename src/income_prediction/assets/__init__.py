import dagster as dg
import mlflow
import mlflow.data
import mlflow.data.pandas_dataset
import mlflow.models
import mlflow.utils
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split

from asec.data import CensusASECMetadata, download_and_filter_census_data
from asec.features import get_income_prediction_features
from asec.model_factory import ModelFactory
from income_prediction.utils.dagster import canonical_lakefs_uri_for_input

from ..resources.configuration import Config, OptunaCVConfig
from ..resources.mlflow_session import MlflowSession
from ..utils.mlflow import LakeFSDatasetSource, log_fairness_metrics
from .fairness import evaluate_fairness
from .model import model_container as model_container
from .monitoring import nannyml_container as nannyml_container
from .monitoring import nannyml_estimator as nannyml_estimator
from .monitoring import reference_dataset as reference_dataset


@dg.asset(io_manager_key="lakefs_io_manager")
def census_asec_dataset(experiment_config: Config):
    """Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria."""
    return download_and_filter_census_data(experiment_config.census_asec_dataset_year)


@dg.asset(io_manager_key="lakefs_io_manager")
def income_prediction_features(
    experiment_config: Config, census_asec_dataset: pd.DataFrame
) -> pd.DataFrame:
    """Pre-processes the Census ASEC dataset for income prediction."""
    return get_income_prediction_features(
        experiment_config.salary_bands, census_asec_dataset
    )


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
        "test_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
    }
)
def train_test_data(
    experiment_config: Config, income_prediction_features: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        income_prediction_features, random_state=experiment_config.random_state
    )
    return train_data, test_data


@dg.asset
def optuna_search_xgb(
    context: dg.AssetExecutionContext,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    optuna_cv_config: OptunaCVConfig,
    optuna_xgb_param_distribution: dg.ResourceParam[
        dict[str, optuna.distributions.BaseDistribution]
    ],
    experiment_config: Config,
):
    model_name = "xgboost-classifier"

    X_train = train_data.drop(columns=CensusASECMetadata.TARGET)
    # Encode categorical features for XGBoost
    for col in CensusASECMetadata.CATEGORICAL_FEATURES:
        X_train[col] = X_train[col].astype("category")
    y_train = train_data[CensusASECMetadata.TARGET]

    optuna_search = optuna.integration.OptunaSearchCV(
        ModelFactory.create_xgb(),
        param_distributions=optuna_xgb_param_distribution,
        **optuna_cv_config.as_dict(),
    )
    optuna_search.fit(X_train, y_train)

    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name=model_name):
            mlflow.autolog(log_datasets=False, log_models=False)
            best_model = optuna_search.best_estimator_
            best_model.fit(X_train, y_train)

            train_ds = mlflow.data.pandas_dataset.from_pandas(
                train_data,
                name="train_data",
                targets=CensusASECMetadata.TARGET,
                source=LakeFSDatasetSource(
                    lakefs_uri=canonical_lakefs_uri_for_input(context, "train_data"),
                    server="localhost:8000",
                ),
            )
            mlflow.log_input(train_ds)

            test_ds = mlflow.data.pandas_dataset.from_pandas(
                test_data,
                name="test_data",
                targets=CensusASECMetadata.TARGET,
                source=LakeFSDatasetSource(
                    lakefs_uri=canonical_lakefs_uri_for_input(context, "test_data"),
                    server="localhost:8000",
                ),
            )
            mlflow.log_input(test_ds)

            mlflow.sklearn.log_model(
                best_model,
                artifact_path="model",
                registered_model_name=model_name,
                code_paths=["src/asec"],
                input_example=train_data.drop(columns=CensusASECMetadata.TARGET).head(
                    5
                ),
            )

            mlflow.evaluate(
                model=best_model.predict,
                data=test_ds,
                model_type="classifier",
                evaluator_config={
                    "log_model_explainability": experiment_config.log_model_explainability,
                },
            )

            # Fairness evaluation
            X_test = test_data.drop(columns=CensusASECMetadata.TARGET)
            context.log.info(test_data.columns)
            y_pred = best_model.predict(X_test)

            fairness_metrics = evaluate_fairness(test_data, y_pred)
            log_fairness_metrics(fairness_metrics)

            return best_model
