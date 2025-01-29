import urllib.request
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from dagster import asset

from income_prediction.census_asec_data_description import CensusASECDataDescription
from income_prediction.resources.configuraton import Config


@asset()
def census_asec_dataset(config: Config) -> pd.DataFrame:
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{config.census_asec_dataset_year}/march/asecpub{config.census_asec_dataset_year % 2000}csv.zip"
    data_file = f"pppub{config.census_asec_dataset_year % 2000}.csv"

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        archive_file = temp_path / "data.zip"
        urllib.request.urlretrieve(url, archive_file)
        zipfile.ZipFile(archive_file).extract(data_file, temp_dir)

        df = pd.read_csv(temp_path / data_file)

        # Apply subsetting from original UCI Adult Income dataset
        df = df[
            (df[CensusASECDataDescription.Column.AGE] >= 16)
            & (df[CensusASECDataDescription.Column.TOTAL_INCOME] > 100)
            & (df[CensusASECDataDescription.Column.HOURS_PER_WEEK] > 0)
            & (df[CensusASECDataDescription.Column.FNLWGT] > 0)
        ]

        return df


if __name__ == "__main__":
    config = Config()

    df = census_asec_dataset(config)
    df.to_csv("data/census_asec_dataset.csv")

    print(df.head())
