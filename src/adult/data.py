from __future__ import annotations

import urllib
import urllib.request
import zipfile
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from sensai import InputOutputData
from sensai.util.cache import pickle_cached
from ucimlrepo import fetch_ucirepo


class AdultData:
    """
    Data provider for the [`Census Income` dataset](https://archive.ics.uci.edu/dataset/2/adult) from UCI repository.
    Also known as `Adult` dataset. The provider loads the data using the [`ucimlrepo`](https://github.com/uci-ml-repo/ucimlrepo) package
    and optionally caches the data using the `pickle` module.

    Args:
        data_path: Optional directory to cache the downloaded result.
            If not provided, the data will be downloaded from the UCI repository directly.
    """

    class Column(str, Enum):
        """
        Enum representing the column names in the original data
        """

        AGE = "age"
        WORK_CLASS = "workclass"
        FNLWGT = "fnlwgt"
        EDUCATION = "education"
        EDUCATION_NUM = "education-num"
        MARITAL_STATUS = "marital-status"
        OCCUPATION = "occupation"
        RELATIONSHIP = "relationship"
        SEX = "sex"
        RACE = "race"
        CAPITAL_GAIN = "capital-gain"
        CAPITAL_LOSS = "capital-loss"
        HOURS_PER_WEEK = "hours-per-week"
        NATIVE_COUNTRY = "native-country"
        INCOME = "income"

    TARGET = Column.INCOME
    CLASS_POSITIVE = ">50K"
    COLS_CATEGORICAL = (
        Column.EDUCATION,
        Column.MARITAL_STATUS,
        Column.NATIVE_COUNTRY,
        Column.RELATIONSHIP,
        Column.SEX,
        Column.RACE,
        Column.WORK_CLASS,
        Column.OCCUPATION,
    )
    COLS_NUMERIC = (
        Column.HOURS_PER_WEEK,
        Column.EDUCATION_NUM,
        Column.AGE,
        Column.CAPITAL_GAIN,
        Column.CAPITAL_LOSS,
    )

    def __init__(self, data_path: str | Path | None = None):
        self._data_path = data_path

        loading_func = fetch_ucirepo

        if data_path is not None:
            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(id=2)

    def load_data_frame(self) -> pd.DataFrame:
        """
        Load the data as a pandas DataFrame.
        """
        df = self._data.data.original
        df.loc[:, self.TARGET] = df[self.TARGET].map(lambda x: x.rstrip("."))
        return df

    def load_input_output_data(self) -> InputOutputData:
        """
        Load the data as an `InputOutputData` object used in the
        [`sensai`](https://github.com/opcode81/sensAI) package.
        """
        all_df = self.load_data_frame()
        return InputOutputData(
            all_df.drop(columns=[self.TARGET]), all_df[[self.TARGET]]
        )


def _fetch_asec_data(
    data_path: str | Path,
    year: int = 2024,
) -> pd.DataFrame:
    """Return the US Census CPS ASEC supplemental dataset for a given year as a DataFrame."""
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march/asecpub{year % 2000}csv.zip"
    data_file = f"pppub{year % 2000}.csv"

    with TemporaryDirectory() as temp_dir:
        archive_file = temp_dir + "/data.zip"
        urllib.request.urlretrieve(url, archive_file)
        zipfile.ZipFile(archive_file).extract(data_file, data_path)
        df = pd.read_csv(data_path / data_file)
        return df


class AdultASECData:
    """
    Data provider for the US Census CPS ASEC supplemental dataset.

    2024 dataset data dictionary: https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asec2024_ddl_pub_full.pdf

    The provider loads the data from the US Census web server and optionally caches the data using the `pickle` module.

    Args:
        data_path: Optional directory to cache the downloaded result.
            If not provided, the data will be downloaded from the US Census web server.
    """

    class Column(str, Enum):
        """
        Enum representing the column names in the original data
        """

        # FIXME: This is a very small subset of the original data
        AGE = "A_AGE"
        HOURS_PER_WEEK = "HRSWK"
        MARITAL_STATUS = "A_MARITL"
        EDUCATION = "A_HGA"
        FNLWGT = "A_FNLWGT"
        SEX = "A_SEX"
        RACE = "PRDTRACE"
        INCOME = "AGI"

    TARGET = Column.INCOME

    COLS_CATEGORICAL = (
        Column.EDUCATION,
        Column.MARITAL_STATUS,
        Column.SEX,
        Column.RACE,
    )
    COLS_NUMERIC = (
        Column.HOURS_PER_WEEK,
        Column.AGE,
        Column.FNLWGT,
    )
    COLS_ORDINAL = ()

    def __init__(self, data_path: str | Path | None = None, year: int = 2024):
        self._data_path = data_path

        loading_func = _fetch_asec_data
        if data_path is not None:
            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(year=year, data_path=data_path)

    def load_data_frame(self) -> pd.DataFrame:
        df = self._data

        # Apply subsetting from original UCI Adult Income dataset
        df = df[
            (df["A_AGE"] >= 16)
            & (df["AGI"] > 100)
            & (df["HRSWK"] > 0)
            & (df["A_FNLWGT"] > 0)
        ]
        return df

    def load_input_output_data(self) -> InputOutputData:
        df = self.load_data_frame()
        return InputOutputData(
            inputs=df[
                [
                    col
                    for col in self.COLS_CATEGORICAL
                    + self.COLS_NUMERIC
                    + self.COLS_ORDINAL
                ]
            ],
            outputs=df[[self.TARGET]],
        )
