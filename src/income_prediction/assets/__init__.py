from tempfile import TemporaryDirectory

import dagster as dg
import mlflow
import mlflow.data
import mlflow.data.pandas_dataset
import mlflow.models
import mlflow.utils
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split

from asec.data import download_pums_data, filter_pums_data, binning_targets, transform_to_categorical, \
  PUMSMetaData

from asec.model_factory import ModelFactory
from income_prediction.utils.dagster import canonical_lakefs_uri_for_input

from ..resources.configuration import Config, OptunaCVConfig
from ..resources.mlflow_session import MlflowSession
from ..utils.mlflow import log_fairness_metrics
from .fairness import evaluate_fairness
from .model import model_container as model_container
from .monitoring import nannyml_container as nannyml_container
from .monitoring import nannyml_estimator as nannyml_estimator
from .monitoring import reference_dataset as reference_dataset


@dg.asset(io_manager_key="lakefs_io_manager", group_name="data_preprocessing")
def pums_raw_data(experiment_config: Config):
  with TemporaryDirectory(delete=False) as temp_dir:
    raw_df = download_pums_data(experiment_config.census_asec_dataset_year, base_dir=temp_dir)
  return raw_df

@dg.multi_asset(
  outs={
    "feature_df": dg.AssetOut(io_manager_key="lakefs_io_manager"),
    "target_df": dg.AssetOut(io_manager_key="lakefs_io_manager"),
  },
  group_name="data_preprocessing",
)
def filtered_pums_data(pums_raw_data: pd.DataFrame):
  return filter_pums_data(pums_raw_data, PUMSMetaData.REASSEMBLED_ADULT_FEATURES)

@dg.asset(io_manager_key="lakefs_io_manager", group_name="data_preprocessing")
def transformed_target(target_df: pd.DataFrame, experiment_config: Config):
  return binning_targets(target_df, experiment_config.salary_bands)

@dg.asset(io_manager_key="lakefs_io_manager", group_name="data_preprocessing")
def transformed_features(feature_df: pd.DataFrame):
  return transform_to_categorical(feature_df)

@dg.asset(io_manager_key="lakefs_io_manager", group_name="data_preprocessing")
def preprocessed_data(transformed_features: pd.DataFrame, transformed_target: pd.DataFrame):
  return pd.concat([transformed_features, transformed_target], axis=1)


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
        "test_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
    },
  group_name="training"
)
def train_test_data(
    experiment_config: Config, preprocessed_data: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        preprocessed_data, random_state=experiment_config.random_state
    )
    return train_data, test_data


@dg.asset(group_name="training")
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

    X_train = train_data.drop(columns=PUMSMetaData.TARGET)
    y_train = train_data[PUMSMetaData.TARGET]
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
                targets=PUMSMetaData.TARGET,
                source=canonical_lakefs_uri_for_input(
                    context, "train_data", protocol="s3"
                ),
            )
            mlflow.log_input(train_ds)

            test_ds = mlflow.data.pandas_dataset.from_pandas(
                test_data,
                name="test_data",
                targets=PUMSMetaData.TARGET,
                source=canonical_lakefs_uri_for_input(
                    context, "test_data", protocol="s3"
                ),
            )
            mlflow.log_input(test_ds)

            mlflow.sklearn.log_model(
                best_model,
                artifact_path="model",
                registered_model_name=model_name,
                code_paths=["src/asec"],
                input_example=train_data.drop(columns=PUMSMetaData.TARGET).head(
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
            X_test = test_data.drop(columns=PUMSMetaData.TARGET)
            context.log.info(test_data.columns)
            y_pred = best_model.predict(X_test)

            fairness_metrics = evaluate_fairness(test_data, y_pred)
            log_fairness_metrics(fairness_metrics)

            return best_model
