from functools import partial

import numpy as np
import pandas as pd

from .data import CensusASECMetadata


def assign_salary_bands(df: pd.DataFrame, salary_bands: list[int]) -> pd.DataFrame:
    """Categorizes individuals into salary bands based on their total annual income.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing individuals' annual income.
    salary_bands : list[int]
        Threshold values defining salary bands.

    Returns
    -------
    pd.DataFrame
        Updated dataset with an additional column indicating the salary band.
    """
    df[CensusASECMetadata.Fields.SALARY_BAND] = np.searchsorted(
        salary_bands, df[CensusASECMetadata.Fields.ANNUAL_INCOME], side="right"
    )

    return df


def binarize_marital_status(df: pd.DataFrame) -> pd.DataFrame:
    """Binarize the marital status attribute by grouping all non-married statuses into a single category."""

    df[CensusASECMetadata.Fields.MARITAL_STATUS] = (
        df[CensusASECMetadata.Fields.MARITAL_STATUS].isin([1, 2, 3, 4]).astype(int)
    )
    return df


def select_features(df: pd.DataFrame, exclude: list[str] = None) -> pd.DataFrame:
    """Filters and retains only the relevant categorical, numerical, ordinal features, and the target variable.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing all raw features.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only selected relevant features and the target value.
    """
    selected_features = (
        CensusASECMetadata.CATEGORICAL_FEATURES
        + CensusASECMetadata.NUMERIC_FEATURES
        + CensusASECMetadata.ORDINAL_FEATURES
        + [CensusASECMetadata.TARGET]
    )

    if exclude is not None:
        selected_features = [feat for feat in selected_features if feat not in exclude]

    return df[selected_features]


def get_income_prediction_features(
    salary_bands: list[int],
    census_asec_dataset: pd.DataFrame,
    exclude: list[str] = None,
) -> pd.DataFrame:
    """Preprocesses the Census ASEC dataset for income prediction by:
        - Assigning salary bands based on income thresholds.
        - Filtering relevant features needed for prediction.

    Parameters
    ----------
    salary_thresholds : list[int]
        Threshold values defining salary bands.
    census_asec_dataset : pd.DataFrame
        The raw Census ASEC supplementary dataset.

    Returns
    -------
    pd.DataFrame
        Preprocessed DataFrame containing selected features and salary band classifications.
    """

    return (
        census_asec_dataset.pipe(assign_salary_bands, salary_bands)
        .pipe(binarize_marital_status)
        .pipe(partial(select_features, exclude=exclude))
    )
