import pandas as pd
from dagster import asset

from income_prediction.census_asec_data_description import CensusASECDataDescription
from income_prediction.resources.census_asec_downloader import CensusASECDownloader


@asset()
def census_asec_dataset(census_data_downloader: CensusASECDownloader) -> pd.DataFrame:
    df = census_data_downloader.download()

    # Apply subsetting from original UCI Adult Income dataset
    df = df[
        (df[CensusASECDataDescription.Column.AGE] >= 16)
        & (df[CensusASECDataDescription.Column.TOTAL_INCOME] > 100)
        & (df[CensusASECDataDescription.Column.HOURS_PER_WEEK] > 0)
        & (df[CensusASECDataDescription.Column.FNLWGT] > 0)
    ]

    return df


if __name__ == "__main__":
    census_data_downloader = CensusASECDownloader(year=2024)

    df = census_asec_dataset(census_data_downloader)
    df.to_csv("data/census_acec_dataset.csv")

    print(df.head())
