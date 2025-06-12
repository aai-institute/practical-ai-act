import pandas as pd

from .data import CensusASECMetadata


def assign_salary_bands(
    df: pd.DataFrame, lower_bound: float, upper_bound: float
) -> pd.DataFrame:
    """Matching individuals to a given salary range based on their total annual income.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing individuals' annual income.
    lower_bound : float
        Lower bound for the acceptable income
    upper_bound : float
        Upper bound for the acceptable income

    Returns
    -------
    pd.DataFrame
        Updated dataset with an additional column indicating the salary band.
    """

    if lower_bound >= upper_bound:
        raise ValueError(
            f"Salary bounds must be ordered, got: ({lower_bound}, {upper_bound})"
        )

    df[CensusASECMetadata.TARGET] = (
        df[CensusASECMetadata.Fields.ANNUAL_INCOME]
        .between(lower_bound, upper_bound)
        .astype(int)
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
