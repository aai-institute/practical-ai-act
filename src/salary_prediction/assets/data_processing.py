from functools import partial

import dagster as dg
import pandas as pd
from dagster_pandas.data_frame import create_table_schema_metadata_from_dataframe

from asec.data import (
    PUMSMetaData,
    download_pums_data,
    filter_pums_data,
    transform_categorical_features,
)
from asec.fairness import extract_metrics
from asec.features import (
    assign_salary_bands,
    select_features,
)

from ..resources.configuration import Config

GROUP_NAME = "data_processing"


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def raw_pums_data(
    context: dg.AssetExecutionContext, experiment_config: Config
) -> pd.DataFrame:
    df = download_pums_data(
        experiment_config.pums_dataset_year,
        random_seed=experiment_config.random_state,
    )
    context.add_output_metadata({
        "num_rows": dg.MetadataValue.int(len(df)),
        "schema": create_table_schema_metadata_from_dataframe(df),
    })
    return df


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def filtered_pums_data(
    context: dg.AssetExecutionContext, raw_pums_data: pd.DataFrame
) -> pd.DataFrame:
    feature_df, target_df = filter_pums_data(
        raw_pums_data, features=PUMSMetaData.FEATURES
    )
    context.add_output_metadata({
        "num_rows": dg.MetadataValue.int(len(feature_df)),
        "schema": create_table_schema_metadata_from_dataframe(feature_df),
    })
    return pd.concat([feature_df, target_df], axis=1)


@dg.asset_check(asset=filtered_pums_data)
def check_filtered_pums_data_colums(
    filtered_pums_data: pd.DataFrame,
) -> dg.AssetCheckResult:
    has_required_columns = all(
        col in filtered_pums_data.columns for col in PUMSMetaData.FEATURES
    )
    has_target_column = PUMSMetaData.ORIGINAL_TARGET in filtered_pums_data.columns
    return dg.AssetCheckResult(passed=has_required_columns and has_target_column)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def transformed_target(
    filtered_pums_data: pd.DataFrame, experiment_config: Config
) -> pd.DataFrame:
    return assign_salary_bands(
        filtered_pums_data,
        experiment_config.salary_lower_bound,
        experiment_config.salary_upper_bound,
    )


@dg.asset_check(asset=transformed_target)
def check_transformed_target(transformed_target: pd.DataFrame) -> dg.AssetCheckResult:
    issues = []

    # Check that the original target column has been transformed correctly and removed
    has_target_column = PUMSMetaData.TARGET in transformed_target.columns
    if not has_target_column:
        issues.append(f"Missing target column: {PUMSMetaData.TARGET}")

    has_no_original_target_column = (
        PUMSMetaData.ORIGINAL_TARGET not in transformed_target.columns
    )
    if not has_no_original_target_column:
        issues.append(
            f"Original target column should not be present: {PUMSMetaData.ORIGINAL_TARGET}"
        )

    # Check domain of the target column
    allowed_values = [0, 1]
    has_correct_values = bool(
        transformed_target[PUMSMetaData.TARGET].isin(allowed_values).all()
    )
    if not has_correct_values:
        issues.append(
            f"Target column {PUMSMetaData.TARGET} should only contain values {allowed_values}, found {transformed_target[PUMSMetaData.TARGET].unique()}."
        )

    if len(issues) == 0:
        description = "Data transformation checks passed."
    else:
        description = "Issues found: \n" + "\n".join(issues)

    return dg.AssetCheckResult(
        passed=has_target_column
        and has_no_original_target_column
        and has_correct_values,
        description=description,
    )


def reindex_by_sensitive_attributes(
    df: pd.DataFrame, sensitive_attributes: list[str]
) -> pd.DataFrame:
    """Index the dataset by sensitive attributes, as expected by the bias mitigation algorithms in AIF360."""
    return df.set_index(sensitive_attributes, drop=False)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def preprocessed_features(
    context: dg.AssetExecutionContext,
    transformed_target: pd.DataFrame,
    experiment_config: Config,
) -> pd.DataFrame:
    df = (
        transformed_target.pipe(select_features)
        .pipe(transform_categorical_features)
        .pipe(
            partial(
                reindex_by_sensitive_attributes,
                sensitive_attributes=experiment_config.protected_attributes.protected_attribute_names,
            )
        )
    )

    context.add_output_metadata({
        "schema": create_table_schema_metadata_from_dataframe(df),
    })

    return df


@dg.asset_check(asset=preprocessed_features)
def check_preprocessed_features_no_na(
    preprocessed_features: pd.DataFrame,
) -> dg.AssetCheckResult:
    has_no_na = not bool(preprocessed_features.isnull().values.any())
    return dg.AssetCheckResult(passed=has_no_na)


@dg.asset(io_manager_key="lakefs_io_manager", group_name=GROUP_NAME, kinds={"pandas"})
def sub_sampled_data(
    context: dg.AssetExecutionContext,
    preprocessed_features: pd.DataFrame,
    experiment_config: Config,
):
    if experiment_config.sample_fraction is None:
        return preprocessed_features

    df = preprocessed_features.sample(
        frac=experiment_config.sample_fraction,
        random_state=experiment_config.random_state,
    )

    context.add_output_metadata({"num_rows": dg.MetadataValue.int(len(df))})

    # Fairness metrics
    # dm = dataset_metrics(df, experiment_config.protected_attributes)
    metrics = extract_metrics(
        y_true=preprocessed_features[PUMSMetaData.TARGET],
        protected_attributes=experiment_config.protected_attributes,
    )
    context.add_asset_metadata(
        metadata={k: dg.MetadataValue.float(v) for k, v in metrics.items()},
    )

    return df
