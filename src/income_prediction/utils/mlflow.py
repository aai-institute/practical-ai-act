from typing import Any

import mlflow
from aif360.metrics import ClassificationMetric


class LakeFSDatasetSource(mlflow.data.DatasetSource):
    """A custom MLflow dataset source for datasets stored in lakeFS"""

    def __init__(self, lakefs_uri: str, server: str):
        super().__init__()
        self.uri = lakefs_uri
        self.server = server

    @staticmethod
    def _get_source_type() -> str:
        return "lakefs"

    def load(self) -> Any:
        raise NotImplementedError()

    @staticmethod
    def _can_resolve(raw_source: Any) -> bool:
        if raw_source is None:
            return False
        if isinstance(raw_source, str):
            return raw_source.startswith("lakefs://")
        return False

    @classmethod
    def _resolve(cls, raw_source: Any) -> "mlflow.data.DatasetSource":
        return cls(raw_source)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self._get_source_type(),
            "lakefs_uri": self.uri,
            "server": self.server,
        }

    @classmethod
    def from_dict(cls, source_dict: dict[Any, Any]) -> "mlflow.data.DatasetSource":
        source_type = source_dict["source_type"]
        if source_type != cls._get_source_type():
            raise ValueError(
                f"Source type {source_dict['source_type']} does not match expected type {cls._get_source_type()}"
            )
        return cls(**source_dict)


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
