from __future__ import annotations

from os import PathLike

import numpy as np
import pandas as pd
from folktables import ACSDataSource, BasicProblem, adult_filter


def download_pums_data(year: int, base_dir: str | PathLike = "data"):
    """
    This function uses the `folktables` library to download
    the Public Use Microdata Sample (PUMS) data from the US Census Bureau.

    Args:
      year: The year for which the PUMS data is to be downloaded.
      base_dir: The base directory where the data will be stored.

    Returns:
      pd.DataFrame: The downloaded PUMS data as a pandas DataFrame.

    """
    data_source = ACSDataSource(
        survey_year=year,
        horizon="1-Year",
        survey="person",
        root_dir=str(base_dir),
    )
    return data_source.get_data(download=True)


def filter_pums_data(
    df: pd.DataFrame, features: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    spec = BasicProblem(
        features=features,
        target=PUMSMetaData.ORIGINAL_TARGET,
        preprocess=adult_filter,
    )

    feature_df, target_df, _ = spec.df_to_pandas(df)
    return feature_df, target_df


def binning_targets(target_df: pd.DataFrame, target_bins: list[int]) -> pd.DataFrame:
    values = np.searchsorted(
        target_bins, target_df[PUMSMetaData.ORIGINAL_TARGET], side="right"
    )
    return pd.DataFrame(data=values, columns=[PUMSMetaData.TARGET])


def transform_categorical_features(feature_df: pd.DataFrame) -> pd.DataFrame:
    """Transforms categorical/ordinal features in the given DataFrame to the 'category' dtype."""

    cat_cols = (
        set(PUMSMetaData.CATEGORICAL_FEATURES)
        .union(PUMSMetaData.ORDINAL_FEATURES)
        .intersection(set(feature_df.columns))
    )
    for col in cat_cols:
        feature_df[col] = feature_df[col].astype("category")

    return feature_df.infer_objects()


class PUMSMetaData:
    class Fields:
        """
        Mapping of original column names to human-readable names for PUMS data.
        """

        # Demographics
        AGE_YEARS = "AGEP"
        SEX = "SEX"
        MARITAL_STATUS = "MAR"
        HOUSEHOLD_RELATIONSHIP = "RELSHIPP"
        HISPANIC_ETHNICITY = "HISP"
        ASIAN_ETHNICITY = "RACASN"
        RACE = "RAC1P"
        COUNTRY_OF_BIRTH = "POBP"
        CITIZENSHIP_STATUS = "CIT"
        DISABILITY_STATUS = "DIS"

        # Education
        EDUCATION_LEVEL = "SCHL"
        ENROLLMENT_STATUS = "SCH"

        # Employment & Work
        EMPLOYMENT_STATUS = "ESR"
        EMPLOYMENT_CLASS = "COW"
        INDUSTRY = "INDP"
        HOURS_PER_WEEK = "WKHP"
        WORK_WEEKS = "WKWN"
        LAST_WORKED = "WKL"
        MAJOR_OCCUPATION = "OCCP"
        ANNUAL_WAGE = "WAGP"

        # Income & Earnings
        ANNUAL_INCOME = "PINCP"

        # Health & Insurance
        HAS_HEALTH_INSURANCE = "HICOV"

    # Target variable
    ORIGINAL_TARGET = Fields.ANNUAL_WAGE
    INCOME_IN_RANGE = "SALARY_IN_RANGE"
    TARGET = INCOME_IN_RANGE

    # Feature categories
    CATEGORICAL_FEATURES = [
        Fields.SEX,
        Fields.RACE,
        Fields.CITIZENSHIP_STATUS,
        Fields.EMPLOYMENT_CLASS,
        Fields.INDUSTRY,
        Fields.MAJOR_OCCUPATION,
        Fields.HAS_HEALTH_INSURANCE,
    ]

    NUMERIC_FEATURES = [
        Fields.WORK_WEEKS,
        Fields.HOURS_PER_WEEK,
        Fields.AGE_YEARS,
    ]

    ORDINAL_FEATURES = [Fields.EDUCATION_LEVEL]

    FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES + ORDINAL_FEATURES
