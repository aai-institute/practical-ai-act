from functools import partial

import dagster as dg
import pandas as pd

from asec.data import (
    PUMSMetaData,
    download_pums_data,
    filter_pums_data,
    transform_to_categorical,
)
from asec.features import (
    assign_salary_bands,
    select_features,
)
from income_prediction.assets.fairness import dataset_metrics

from ..resources.configuration import Config

GROUP_NAME = "data_processing"


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def raw_pums_data(experiment_config: Config) -> pd.DataFrame:
    return download_pums_data(experiment_config.pums_dataset_year)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def filtered_pums_data(raw_pums_data: pd.DataFrame) -> pd.DataFrame:
    feature_df, target_df = filter_pums_data(
        raw_pums_data, features=PUMSMetaData.FEATURES
    )
    return pd.concat([feature_df, target_df], axis=1)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def transformed_target(
    filtered_pums_data: pd.DataFrame, experiment_config: Config
) -> pd.DataFrame:
    return assign_salary_bands(
        filtered_pums_data,
        experiment_config.salary_lower_bound,
        experiment_config.salary_upper_bound,
    )


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def preprocessed_features(transformed_target: pd.DataFrame) -> pd.DataFrame:
    return transformed_target.pipe(
        partial(select_features, exclude=[PUMSMetaData.ORIGINAL_TARGET])
    ).pipe(transform_to_categorical)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def sub_sampled_data(preprocessed_features: pd.DataFrame, experiment_config: Config):
    if experiment_config.sample_fraction is None:
        return preprocessed_features

    return preprocessed_features.sample(
        frac=experiment_config.sample_fraction,
        random_state=experiment_config.random_state,
    )


@dg.asset(group_name=GROUP_NAME)
def dataset_fairness_metrics(sub_sampled_data: pd.DataFrame):
    """
    Evaluates fairness metrics for the processed dataset.
    """
    from aif360.metrics import BinaryLabelDatasetMetric

    metric_fns = [
        BinaryLabelDatasetMetric.disparate_impact,
        BinaryLabelDatasetMetric.statistical_parity_difference,
        BinaryLabelDatasetMetric.mean_difference,
    ]
    dm = dataset_metrics(sub_sampled_data)
    metrics = {}
    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn(dm)
        metrics[metric_name] = metric_value

    print("Dataset Fairness Metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  - {metric_name}: {metric_value}")

    return metrics
