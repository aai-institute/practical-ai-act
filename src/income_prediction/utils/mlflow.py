import mlflow
import mlflow.sklearn
from aif360.metrics import ClassificationMetric
from fairlearn.metrics import MetricFrame

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

    # Metrics that operate separately on privileged and unprivileged groups
    for metric_name in [
        "true_positive_rate",
        "false_positive_rate",
        "true_negative_rate",
        "false_negative_rate",
    ]:
        metric_value = getattr(fairness_metrics, metric_name)(privileged=True)
        mlflow.log_metric(f"{prefix}{metric_name}_privileged", metric_value)

        metric_value = getattr(fairness_metrics, metric_name)(privileged=False)
        mlflow.log_metric(f"{prefix}{metric_name}_unprivileged", metric_value)


def log_fairness_metrics_by_group(mf: MetricFrame, prefix: str = "fair_"):
    """Logs Fairlearn fairness metrics by group to MLflow."""

    for metric_col in mf.by_group.columns:
        if mf.by_group.index.nlevels > 1:
            for group_index in mf.by_group[metric_col].index:
                attribute_name = "_".join(mf.by_group.index.names)
                group_name = "_".join(map(str, group_index))
                metric_value = mf.by_group[metric_col][group_index]
                mlflow.log_metric(
                    f"{prefix}{metric_col}_{attribute_name}_{group_name}",
                    metric_value,
                )

        else:
            attribute_name = mf.by_group.index.names[0]
            for group_name in mf.by_group[metric_col].index:
                metric_value = mf.by_group[metric_col][group_name]
                mlflow.log_metric(
                    f"{prefix}{metric_col}_{attribute_name}_{group_name}", metric_value
                )

    plt = mf.by_group.plot(
        kind="bar",
        title="Fairness Metrics by Group",
        subplots=True,
        legend=False,
        figsize=(12, 8),
    )
    mlflow.log_figure(plt[0].figure, "fairness_metrics_by_group.png")


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
