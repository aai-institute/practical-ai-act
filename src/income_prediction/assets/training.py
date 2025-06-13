from typing import TYPE_CHECKING

import dagster as dg
import matplotlib.pyplot as plt
import mlflow
import optuna
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from asec.data import PUMSMetaData

from ..resources.configuration import Config, OptunaCVConfig
from ..resources.mlflow_session import MlflowSession
from ..types import ModelVersion
from ..utils.dagster import canonical_lakefs_uri_for_input
from ..utils.mlflow import (
    log_fairness_metrics,
    log_fairness_metrics_by_group,
)
from .fairness import classification_metrics, make_metricframe

if TYPE_CHECKING:
    import mlflow.data.pandas_dataset
    import mlflow.models
    import mlflow.sklearn

GROUP_NAME = "training"


def _log_datasets(
    context: dg.AssetExecutionContext,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
):
    train_ds = mlflow.data.pandas_dataset.from_pandas(
        train_data,
        name="train_data",
        targets=PUMSMetaData.TARGET,
        source=canonical_lakefs_uri_for_input(context, "train_data", protocol="s3"),
    )
    mlflow.log_input(train_ds)

    test_ds = mlflow.data.pandas_dataset.from_pandas(
        test_data,
        name="test_data",
        targets=PUMSMetaData.TARGET,
        source=canonical_lakefs_uri_for_input(context, "test_data", protocol="s3"),
    )
    mlflow.log_input(test_ds)


def _log_evaluation(
    model,
    test_data: pd.DataFrame,
    /,
    evaluator_config: dict,
):
    mlflow.evaluate(
        model=model.predict,
        data=test_data,
        model_type="classifier",
        targets=PUMSMetaData.TARGET,
        evaluator_config=evaluator_config,
    )


def _log_fairness_evaluation(
    test_data: pd.DataFrame, y_pred: pd.Series, sensitive_feature_names: list[str]
):
    # -- AIF360
    fairness_metrics = classification_metrics(test_data, y_pred)
    log_fairness_metrics(fairness_metrics)

    # -- Fairlearn
    sensitive_features = test_data[sensitive_feature_names]
    mf = make_metricframe(test_data, y_pred, sensitive_features=sensitive_features)
    log_fairness_metrics_by_group(mf)


def _log_explainability_plots(model, x_test: pd.DataFrame):
    plt.close()

    explainer = shap.Explainer(model, x_test, algorithm="tree")
    shap_values = explainer(x_test)

    ax = shap.plots.bar(shap_values, show=False)
    mlflow.log_figure(ax.figure, "shap_bar_plot.png")
    plt.close()

    ax = shap.plots.violin(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_violin_plot.png")
    plt.close()


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="lakefs_io_manager", kinds={"pandas"}),
        "test_data": dg.AssetOut(io_manager_key="lakefs_io_manager", kinds={"pandas"}),
    },
    group_name=GROUP_NAME,
)
def train_test_data(
    experiment_config: Config, sub_sampled_data: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        sub_sampled_data,
        random_state=experiment_config.random_state,
        test_size=experiment_config.test_size,
    )
    return train_data, test_data


@dg.asset(group_name=GROUP_NAME, kinds={"xgboost"})
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
) -> ModelVersion:
    model_name = "xgboost-classifier"

    X_train = train_data.drop(columns=PUMSMetaData.TARGET)
    y_train = train_data[PUMSMetaData.TARGET]

    optuna_search = optuna.integration.OptunaSearchCV(
        XGBClassifier(enable_categorical=True),
        param_distributions=optuna_xgb_param_distribution,
        **optuna_cv_config.as_dict(),
    )
    optuna_search.fit(X_train, y_train)

    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name=model_name):
            # We log datasets and models explicitly below
            mlflow.autolog(log_datasets=False, log_models=False)

            best_model = optuna_search.best_estimator_
            best_model.fit(X_train, y_train)

            X_test = test_data.drop(columns=PUMSMetaData.TARGET)
            y_pred = best_model.predict(X_test)

            _log_datasets(context, train_data, test_data)
            _log_evaluation(
                best_model,
                test_data,
                evaluator_config={"log_model_explainability": False},
            )

            # Fairness evaluation
            _log_fairness_evaluation(
                test_data,
                y_pred,
                sensitive_feature_names=experiment_config.sensitive_feature_names,
            )

            # Explainability plots
            _log_explainability_plots(best_model, X_test)

            # Model registration
            signature = mlflow.models.infer_signature(
                X_train.head(5), best_model.predict(X_train.head(5))
            )

            model_info = mlflow.sklearn.log_model(
                best_model,
                artifact_path="model",
                registered_model_name=model_name,
                signature=signature,
                code_paths=["src/asec"],
                input_example=train_data.drop(columns=PUMSMetaData.TARGET).head(5),
            )

            return ModelVersion(
                version=str(model_info.registered_model_version),
                name=model_name,
                uri=model_info.model_uri,
            )
