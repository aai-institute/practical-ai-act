import mlflow
import mlflow.sklearn
from aif360.metrics import ClassificationMetric

from income_prediction.types import ModelVersion


def start_mlflow_run(
    run_name: str, tags: dict[str, str] | None = None
) -> mlflow.ActiveRun:
    """Starts a new MLflow run or retrieves an existing run with the specified run name.

    Parameters
    ----------
    run_name : str
        Name of the MLflow run.
    tags : dict[str, str], optional
        A dictionary of tags to associate with the MLflow run. Defaults to None.

    Returns
    -------
    mlflow.ActiveRun
        The active MLflow run.
    """

    if tags is None:
        tags = {}

    active_run = mlflow.active_run()
    if active_run:
        return active_run

    existing_runs = mlflow.search_runs(
        filter_string=f"attributes.`run_name`='{run_name}'", output_format="list"
    )

    if existing_runs:
        run_id = existing_runs[0].info.run_id
        return mlflow.start_run(run_id=run_id)

    return mlflow.start_run(run_name=run_name, tags=tags)


def log_fairness_metrics(fairness_metrics: ClassificationMetric, prefix: str = "fair_"):
    """Logs AIF360 classification fairness metrics to MLflow."""
    metric_fns = [
        ClassificationMetric.statistical_parity_difference,
        ClassificationMetric.disparate_impact,
        ClassificationMetric.equal_opportunity_difference,
        ClassificationMetric.average_abs_odds_difference,
    ]

    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn(fairness_metrics)
        mlflow.log_metric(f"{prefix}{metric_name}", metric_value)

    mlflow.log_metric(
        f"{prefix}tpr_privileged",
        fairness_metrics.true_positive_rate(privileged=True),
    )
    mlflow.log_metric(
        f"{prefix}tpr_unprivileged",
        fairness_metrics.true_positive_rate(privileged=False),
    )


def load_model(version: ModelVersion):
    """Downloads the model from MLflow and returns the local path.

    Parameters
    ----------
    version : ModelVersion
        The version of the model to download.

    Returns
    -------
    str
        The local path to the downloaded model.
    """
    return mlflow.sklearn.load_model(version.uri)
