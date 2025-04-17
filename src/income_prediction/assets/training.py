import dagster as dg
import mlflow
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split

from asec.data import CensusASECMetadata
from asec.model_factory import ModelFactory

from ..resources.configuration import Config
from ..resources.mlflow_session import MlflowSession
from .fairness import evaluate_fairness
from ..resources.configuration import OptunaCVConfig
from ..utils.dagster import canonical_lakefs_uri_for_input
from ..utils.mlflow import log_fairness_metrics

GROUP_NAME = "training"


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
        "test_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
    },
    group_name=GROUP_NAME,
)
def train_test_data(
    experiment_config: Config, preprocessed_features: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        preprocessed_features,
        random_state=experiment_config.random_state,
        test_size=experiment_config.test_size,
    )
    return train_data, test_data


@dg.asset(group_name=GROUP_NAME)
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
                source=canonical_lakefs_uri_for_input(
                    context, "train_data", protocol="s3"
                ),
            )
            mlflow.log_input(train_ds)

            test_ds = mlflow.data.pandas_dataset.from_pandas(
                test_data,
                name="test_data",
                targets=CensusASECMetadata.TARGET,
                source=canonical_lakefs_uri_for_input(
                    context, "test_data", protocol="s3"
                ),
            )
            mlflow.log_input(test_ds)

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

            mlflow.sklearn.log_model(
                best_model,
                artifact_path="model",
                registered_model_name=model_name,
                code_paths=["src/asec"],
                input_example=train_data.drop(columns=CensusASECMetadata.TARGET).head(
                    5
                ),
            )

            return best_model
