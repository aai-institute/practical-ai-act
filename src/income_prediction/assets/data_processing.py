import dagster as dg
import pandas as pd

from asec.data import download_census_data, filter_relevant_census_data
from asec.features import (
    assign_salary_bands,
    binarize_marital_status,
    select_features,
)
from income_prediction.assets.fairness import dataset_metrics

from ..resources.configuration import Config

GROUP_NAME = "data_processing"


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def raw_asec_data(experiment_config: Config) -> pd.DataFrame:
    return download_census_data(
        experiment_config.census_asec_dataset_year,
        use_archive=experiment_config.census_asec_dataset_use_archive,
    )


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def filtered_asec_data(raw_asec_data: pd.DataFrame) -> pd.DataFrame:
    return filter_relevant_census_data(raw_asec_data)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def transformed_target(
    filtered_asec_data: pd.DataFrame, experiment_config: Config
) -> pd.DataFrame:
    return assign_salary_bands(filtered_asec_data, experiment_config.salary_bands)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def preprocessed_features(transformed_target: pd.DataFrame) -> pd.DataFrame:
    return transformed_target.pipe(binarize_marital_status).pipe(select_features)


@dg.asset(group_name=GROUP_NAME)
def dataset_fairness_metrics(preprocessed_features: pd.DataFrame):
    """
    Evaluates fairness metrics for the processed dataset.
    This is a placeholder asset that can be extended to log or return fairness metrics.
    """
    from aif360.metrics import BinaryLabelDatasetMetric

    metric_fns = [
        BinaryLabelDatasetMetric.disparate_impact,
        BinaryLabelDatasetMetric.statistical_parity_difference,
        BinaryLabelDatasetMetric.consistency,
        BinaryLabelDatasetMetric.mean_difference,
        BinaryLabelDatasetMetric.smoothed_empirical_differential_fairness,
    ]
    dm = dataset_metrics(preprocessed_features)
    metrics = {}
    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn(dm)
        metrics[metric_name] = metric_value

    print("Dataset Fairness Metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  - {metric_name}: {metric_value}")

    return metrics
