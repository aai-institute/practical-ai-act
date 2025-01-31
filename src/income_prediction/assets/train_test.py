import pandas as pd
from dagster import AssetOut, multi_asset
from sklearn.model_selection import train_test_split

from income_prediction.config import RANDOM_STATE


@multi_asset(
    outs={
        "train_data": AssetOut(io_manager_key="csv_io_manager"),
        "test_data": AssetOut(io_manager_key="csv_io_manager"),
    }
)
def train_test_data(census_asec_features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets.

    Parameters
    ----------
    census_asec_features : pd.DataFrame
        The preprocessed Census ASEC dataset with the selected features and target values.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        The training and test sets.
    """
    train_data, test_data = train_test_split(census_asec_features, random_state=RANDOM_STATE)
    return train_data, test_data
