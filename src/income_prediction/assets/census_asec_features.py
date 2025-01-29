import bisect

import pandas as pd
from dagster import asset

from income_prediction.census_asec_data_description import CensusASECDataDescription
from income_prediction.config import SalaryBand

SALARY_BANDS = [band.value for band in SalaryBand]


def get_salary_band(row: pd.Series) -> int:
    # bisect.bisect returns the index of the right interval bound that the total income
    # falls into, which equals our desired salary band cutoff.
    total_income = row[CensusASECDataDescription.Column.TOTAL_INCOME]
    return bisect.bisect(SALARY_BANDS, total_income)


@asset()
def census_asec_features(census_asec_dataset: pd.DataFrame) -> pd.DataFrame:
    census_asec_dataset["SALARY_BAND"] = census_asec_dataset.apply(get_salary_band, axis=1)

    df = census_asec_dataset[
        [
            col
            for col in CensusASECDataDescription.COLS_CATEGORICAL
            + CensusASECDataDescription.COLS_NUMERIC
            + CensusASECDataDescription.COLS_ORDINAL
            + (CensusASECDataDescription.TARGET,)
        ]
    ]

    return df


if __name__ == "__main__":
    census_asec_dataset = pd.read_csv("data/census_asec_dataset.csv", index_col=0)

    df = census_asec_features(census_asec_dataset)
    df.to_csv("data/census_asec_features.csv")

    print(df.head())
