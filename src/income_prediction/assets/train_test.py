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
    train_data, test_data = train_test_split(census_asec_features, random_state=RANDOM_STATE)
    return train_data, test_data


if __name__ == "__main__":
    census_asec_features = pd.read_csv("data/census_asec_features.csv", index_col=0)

    train_data, test_data = train_test_data(census_asec_features)

    train_data.to_csv("data/train_data.csv")
    test_data.to_csv("data/test_data.csv")

    print(train_data.head())
    print(test_data.head())
