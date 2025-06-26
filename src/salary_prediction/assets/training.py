from typing import TYPE_CHECKING

import dagster as dg
import matplotlib.pyplot as plt
import mlflow
import optuna
import pandas as pd
import shap
from sklearn.model_selection import train_test_split

from asec.data import PUMSMetaData
from asec.fairness import (
    ProtectedAttributes,
    fairness_metrics,
)
from asec.model_factory import ModelFactory

from ..resources.configuration import Config, OptunaCVConfig
from ..resources.mlflow_session import MlflowSession
from ..types import ModelVersion
from ..utils.dagster import canonical_lakefs_uri_for_input

if TYPE_CHECKING:
    import mlflow.data.pandas_dataset
    import mlflow.models.model
    import mlflow.shap
    import mlflow.sklearn

GROUP_NAME = "model"


def _log_datasets(
    context: dg.AssetExecutionContext,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> tuple[
    mlflow.data.pandas_dataset.PandasDataset,
    mlflow.data.pandas_dataset.PandasDataset,
]:
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

    return train_ds, test_ds


def _log_evaluation(
    model_uri,
    test_data: mlflow.data.pandas_dataset.PandasDataset,
    /,
    evaluator_config: dict,
):
    mlflow.evaluate(
        model=model_uri,
        data=test_data,
        model_type="classifier",
        evaluator_config=evaluator_config,
    )


def _log_fairness_evaluation(
    test_data: pd.DataFrame,
    y_pred: pd.Series,
    protected_attributes: ProtectedAttributes,
    prefix: str = "fair_",
):
    metrics = fairness_metrics(
        y_true=test_data[PUMSMetaData.TARGET],
        y_pred=y_pred,
        prot_attr=protected_attributes,
    )
    for name, val in metrics.items():
        mlflow.log_metric(f"{prefix}{name}", val)


def _create_explainer(
    model, X_test: pd.DataFrame, experiment_config: Config
) -> shap.Explainer:
    plt.close()

    explainer = shap.Explainer(
        model,
        X_test,
        algorithm="permutation",  # TreeExplainer cannot be serialized correctly, see https://github.com/shap/shap/issues/2122
        seed=experiment_config.random_state,
    )

    mlflow.shap.log_explainer(
        explainer,
        name="explainer",
        serialize_model_using_mlflow=False,
    )

    # Calculate feature importance on a subsample of the test set
    n_rows = min(2000, len(X_test))
    expl_df = X_test.sample(n_rows, random_state=experiment_config.random_state)
    shap_values = explainer(expl_df)

    ax = shap.plots.bar(shap_values, show=False)
    mlflow.log_figure(ax.figure, "shap_bar_plot.png")
    plt.close()

    ax = shap.plots.violin(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_violin_plot.png")
    plt.close()

    return explainer


def _register_model(
    model,
    model_name: str,
    X_train: pd.DataFrame,
    tags: dict[str, str] | None = None,
) -> mlflow.models.model.ModelInfo:
    """
    Register the model in MLflow.
    """
    signature = mlflow.models.infer_signature(
        X_train.head(),
        model.predict(X_train.head()),
    )

    model_info = mlflow.sklearn.log_model(
        model,
        name=model_name,
        registered_model_name=model_name,
        signature=signature,
        params=model.get_params(),
        tags=tags,
    )

    # Also include parameters in the run metadata (MLflow >3 only logs them with the model)
    mlflow.log_params(model.get_params())

    return model_info


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
        df = locals()[asset_key]
        metrics = fairness_metrics(
            y_true=df[PUMSMetaData.TARGET],
            prot_attr=experiment_config.protected_attributes,
        )
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
    X_train = train_data.drop(columns=PUMSMetaData.TARGET)
    y_train = train_data[PUMSMetaData.TARGET]

    clf = ModelFactory.create_xgb(
        experiment_config.random_state,
        experiment_config.mitigate_bias,
        experiment_config.protected_attributes.attribute_names,
    )

    optuna_search = optuna.integration.OptunaSearchCV(
        clf,
        param_distributions=optuna_xgb_param_distribution,
        **optuna_cv_config.as_dict(),
    )
    optuna_search.fit(X_train, y_train)

    with mlflow_session.start_run(context):
        best_model = optuna_search.best_estimator_

        mlflow.log_params(experiment_config.model_dump())

        X_test = test_data.drop(columns=PUMSMetaData.TARGET)
        y_pred = best_model.predict(X_test)

        # Model registration
        tags = {
            "bias_mitigation": str(experiment_config.mitigate_bias),
        }
        model_info = _register_model(
            best_model, experiment_config.model_name, X_train, tags
        )

        _, test_ds = _log_datasets(context, train_data, test_data)

        # Model performance evaluation
        _log_evaluation(
            model_info.model_uri,
            test_ds,
            evaluator_config={"log_model_explainability": False},
        )

        # Fairness evaluation
        _log_fairness_evaluation(
            test_data,
            y_pred,
            protected_attributes=experiment_config.protected_attributes,
        )

        # Explainability plots
        if experiment_config.log_model_explainability:
            _create_explainer(best_model.predict, X_test, experiment_config)

        return ModelVersion(
            version=str(model_info.registered_model_version),
            name=experiment_config.model_name,
            uri=model_info.model_uri,
        )
