import dagster as dg
import pandas as pd

from asec.data import download_census_data, filter_relevant_census_data
from asec.features import assign_salary_bands, binarize_marital_status, select_features

from ..resources.configuration import Config

GROUP_NAME = "data_processing"


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME)
def raw_asec_data(experiment_config: Config):
    return download_census_data(
        experiment_config.census_asec_dataset_year,
        use_archive=experiment_config.census_asec_dataset_use_archive,
    )


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME)
def filtered_asec_data(raw_asec_data: pd.DataFrame):
    return filter_relevant_census_data(raw_asec_data)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME)
def transformed_target(filtered_asec_data: pd.DataFrame, experiment_config: Config):
    return assign_salary_bands(filtered_asec_data, experiment_config.salary_bands)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME)
def preprocessed_features(transformed_target: pd.DataFrame):
    return transformed_target.pipe(binarize_marital_status).pipe(select_features)
