from typing import TYPE_CHECKING

import dagster as dg
import matplotlib.pyplot as plt
import mlflow
import optuna
import pandas as pd
import shap
import sklearn
from aif360.sklearn.preprocessing import Reweighing, ReweighingMeta
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
from .fairness import (
    classification_metrics,
    dataset_metrics,
    extract_metrics,
    make_metricframe,
)

if TYPE_CHECKING:
    import mlflow.data.pandas_dataset
    import mlflow.models
    import mlflow.sklearn

GROUP_NAME = "model"


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
    test_data: pd.DataFrame,
    y_pred: pd.Series,
    sensitive_feature_names: list[str],
    prefix: str = "fair_",
):
    # -- AIF360
    fairness_metrics = classification_metrics(test_data, y_pred)
    log_fairness_metrics(fairness_metrics, prefix=prefix)

    # -- Fairlearn
    sensitive_features = test_data[sensitive_feature_names]
    mf = make_metricframe(test_data, y_pred, sensitive_features=sensitive_features)
    log_fairness_metrics_by_group(mf, prefix=prefix)


def _log_explainability_plots(model, X_test: pd.DataFrame, experiment_config: Config):
    plt.close()

    explainer = shap.PermutationExplainer(
        model, X_test, seed=experiment_config.random_state
    )

    # Calculate feature importance on a sample of the test set
    n_rows = min(2000, len(X_test))
    shap_values = explainer(X_test.sample(n_rows))

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
    context: dg.AssetExecutionContext,
    experiment_config: Config,
    sub_sampled_data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        sub_sampled_data,
        random_state=experiment_config.random_state,
        test_size=experiment_config.test_size,
    )

    # Fairness metrics
    for asset_key in ["train_data", "test_data"]:
        dm = dataset_metrics(locals()[asset_key])
        metrics = extract_metrics(dm)
        context.add_asset_metadata(asset_key=asset_key, metadata=metrics)

    return train_data, test_data


@dg.asset(group_name=GROUP_NAME, kinds={"xgboost"})
def optuna_search_xgb(
    context: dg.AssetExecutionContext,
    mlflow_session: MlflowSession,
    optuna_cv_config: OptunaCVConfig,
    optuna_xgb_param_distribution: dg.ResourceParam[
        dict[str, optuna.distributions.BaseDistribution]
    ],
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    experiment_config: Config,
) -> ModelVersion:
    model_name = "xgboost-classifier"

    sklearn.set_config(enable_metadata_routing=True)

    X_train = train_data.drop(columns=PUMSMetaData.TARGET)
    y_train = train_data[PUMSMetaData.TARGET]

    clf = XGBClassifier(enable_categorical=True)
    reweighing = ReweighingMeta(
        estimator=clf, reweigher=Reweighing(experiment_config.sensitive_feature_names)
    )

    optuna_search = optuna.integration.OptunaSearchCV(
        reweighing,
        param_distributions=optuna_xgb_param_distribution,
        **optuna_cv_config.as_dict(),
    )
    optuna_search.fit(X_train, y_train)

    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name=model_name):
            # We log datasets and models explicitly below
            mlflow.autolog(log_datasets=False, log_models=False)

            best_model = optuna_search.best_estimator_

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
            if experiment_config.log_model_explainability:
                _log_explainability_plots(
                    best_model.predict_proba, X_test, experiment_config
                )

            # Model registration
            signature = mlflow.models.infer_signature(
                X_train.head(),
                best_model.predict(X_train.head()),
            )

            model_info = mlflow.sklearn.log_model(
                best_model,
                artifact_path="model",
                registered_model_name=model_name,
                signature=signature,
                input_example=X_train.head(5),
            )

            return ModelVersion(
                version=str(model_info.registered_model_version),
                name=model_name,
                uri=model_info.model_uri,
            )
