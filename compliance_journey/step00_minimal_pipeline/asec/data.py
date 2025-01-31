from __future__ import annotations

from enum import Enum
from pathlib import Path

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
