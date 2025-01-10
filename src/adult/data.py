from pathlib import Path

from sensai import InputOutputData
from ucimlrepo import fetch_ucirepo
from sensai.util.cache import pickle_cached


COL_AGE = "age"
COL_WORKCLASS = "workclass"
COL_FNLWGT = "fnlwgt"
COL_EDUCATION = "education"
COL_EDUCATION_NUM = "education-num"
COL_MARITAL_STATUS = "marital-status"
COL_OCCUPATION = "occupation"
COL_RELATIONSHIP = "relationship"
COL_RACE = "race"
COL_SEX = "sex"
COL_CAPITAL_GAIN = "capital-gain"
COL_CAPITAL_LOSS = "capital-loss"
COL_HOURS_PER_WEEK = "hours-per-week"
COL_NATIVE_COUNTRY = "native-country"
COL_INCOME = "income"

COL_TARGET = COL_INCOME

COLS_ALL = (
    COL_AGE,
    COL_WORKCLASS,
    COL_FNLWGT,
    COL_EDUCATION,
    COL_EDUCATION_NUM,
    COL_MARITAL_STATUS,
    COL_OCCUPATION,
    COL_RELATIONSHIP,
    COL_RACE,
    COL_SEX,
    COL_CAPITAL_GAIN,
    COL_CAPITAL_LOSS,
    COL_HOURS_PER_WEEK,
    COL_NATIVE_COUNTRY,
    COL_INCOME,
)

COLS_FEATURE_ALL = tuple([col for col in COLS_ALL if col != COL_TARGET])
COLS_FEATURE_NUMERIC = (
    COL_AGE,
    COL_EDUCATION_NUM,
    COL_CAPITAL_GAIN,
    COL_CAPITAL_LOSS,
    COL_HOURS_PER_WEEK,
)
COLS_FEATURE_CATEGORICAL = tuple(
    [
        col
        for col in COLS_FEATURE_ALL
        if col not in COLS_FEATURE_NUMERIC and col != COL_FNLWGT
    ]
)
CLASS_POSITIVE = ">50K"


class AdultData:
    def __init__(self, data_path: str | Path | None = None):
        self._data_path = data_path

        loading_func = fetch_ucirepo

        if data_path is not None:
            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(id=2)

    def load_data_frame(self):
        df = self._data.data.original
        df.loc[:, COL_TARGET] = df[COL_TARGET].map(lambda x: x.rstrip("."))
        return df

    def load_input_output_data(self):
        all_df = self.load_data_frame()
        return InputOutputData(all_df.drop(columns=[COL_TARGET]), all_df[[COL_TARGET]])
