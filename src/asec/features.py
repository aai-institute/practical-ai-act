import collections.abc
from copy import copy
from enum import Enum
from typing import Literal, Any, Callable

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline, FeatureUnion, make_union, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer, ColumnTransformer

from .data import AdultData, CensusASECMetadata


class MappedColumn(BaseEstimator, TransformerMixin):
    def __init__(self, column: str, mapping: dict, unknown_default: Any = pd.NA):
        """
        Parameters:
        - column: str, the column to map
        - mapping_dict: dict, the dictionary with mapping values
        - unknown_default:
        """
        self.unknown_default = unknown_default
        self.column = column
        self.mapping = mapping

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[self.column].apply(self._map_value).to_frame()

    def _map_value(self, val):
        if isinstance(self.mapping, collections.abc.Mapping):
            if val in set(self.mapping.values()):
                return val

            return self.mapping.get(val, self.unknown_default)
        elif isinstance(self.mapping, Callable):
            return self.mapping(val)
        else:
            raise RuntimeError(f"Unknown mapping type: {type(self.mapping)}")

    def get_feature_names_out(self, input_features):
        return [self.column]


class ColumnDifference(BaseEstimator, TransformerMixin):
    def __init__(self, col1: str, col2: str, resulting_col_name: str):
        self.resulting_col_name = resulting_col_name
        self.col1 = col1
        self.col2 = col2

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return (X[self.col1] - X[self.col2]).to_frame(self.resulting_col_name)


def _encoded_name(name: str) -> str:
    return f"{name}-encoded"


def _standardized_name(name: str) -> str:
    return f"{name}-standardized"


class FeatureName(Enum):
    NET_CAPITAL_STANDARDIZED = _standardized_name("net-capital")
    WORK_CLASS_ENCODED = _encoded_name(AdultData.Column.WORK_CLASS)
    OCCUPATION_ENCODED = _encoded_name(AdultData.Column.OCCUPATION)
    RACE_ENCODED = _encoded_name(AdultData.Column.RACE)
    SEX_ENCODED = _encoded_name(AdultData.Column.SEX)
    AGE_STANDARDIZED = _standardized_name(AdultData.Column.AGE)
    RELATIONSHIP_ENCODED = _encoded_name(AdultData.Column.RELATIONSHIP)
    NATIVE_COUNTRY_ENCODED = _encoded_name(AdultData.Column.NATIVE_COUNTRY)
    MARITAL_STATUS_ENCODED = _encoded_name(AdultData.Column.MARITAL_STATUS)
    EDUCATION_ENCODED = _encoded_name(AdultData.Column.EDUCATION)
    EDUCATION_NUM_STANDARDIZED = _standardized_name(AdultData.Column.EDUCATION_NUM)
    HOURS_PER_WEEK_STANDARDIZED = _standardized_name(AdultData.Column.HOURS_PER_WEEK)


def make_one_hot_encoded(
    column: AdultData.Column,
    mapping_dict: dict | None = None,
    unknown_value: Any | None = None,
    categories: list[str] | Literal["auto"] = "auto",
) -> Pipeline | ColumnTransformer:
    if mapping_dict is None and unknown_value is not None:
        raise ValueError("Must specify mapping when providing unknown default value")

    if categories == "auto" and mapping_dict is not None:
        categories = set(mapping_dict.values())
        if unknown_value is not None:
            categories = categories.union({unknown_value})
        categories = [[*categories]]  # OneHotEncoder expects a list of array-like
    elif categories != "auto":
        categories = [[*categories]]

    encoder = OneHotEncoder(categories=categories)
    if mapping_dict is not None:
        return make_pipeline(
            MappedColumn(column.value, mapping_dict, unknown_default=unknown_value),
            encoder,
        )

    return make_column_transformer((encoder, [column.value]))


def make_standardized(
    column: AdultData.Column,
):
    return make_column_transformer((StandardScaler(), [column.value]))


_all_features: dict[FeatureName, ColumnTransformer | Pipeline] = {}

_all_features[FeatureName.SEX_ENCODED] = make_one_hot_encoded(
    AdultData.Column.SEX, categories=["Female", "Male"]
)


_RACE_MAPPING = {
    "White": "White",
    "Black": "Other",
    "Asian-Pac-Islander": "Other",
    "Amer-Indian-Eskimo": "Other",
    "Other": "Other",
}

_all_features[FeatureName.RACE_ENCODED] = make_one_hot_encoded(
    AdultData.Column.RACE, mapping_dict=_RACE_MAPPING
)


_MARITAL_STATUS_MAPPING = {
    "Married-civ-spouse": "Married",
    "Married-spouse-absent": "Married",
    "Married-AF-spouse": "Married",
    "Never-married": "Never Married",
    "Divorced": "Previously Married",
    "Separated": "Previously Married",
    "Widowed": "Previously Married",
}

_all_features[FeatureName.MARITAL_STATUS_ENCODED] = make_one_hot_encoded(
    AdultData.Column.MARITAL_STATUS, _MARITAL_STATUS_MAPPING
)

_COUNTRY_MAPPING = {"United-States": "US", "?": "Unknown"}
_OTHER_COUNTRY_DEFAULT = "Other"

_all_features[FeatureName.NATIVE_COUNTRY_ENCODED] = make_one_hot_encoded(
    AdultData.Column.NATIVE_COUNTRY,
    _COUNTRY_MAPPING,
    unknown_value=_OTHER_COUNTRY_DEFAULT,
)


_EDUCATION_MAPPING = {
    "Preschool": "No formal education",
    "1st-4th": "No formal education",
    "5th-6th": "No formal education",
    "7th-8th": "No formal education",
    "9th": "Some High School",
    "10th": "Some High School",
    "11th": "Some High School",
    "12th": "Some High School",
    "HS-grad": "High School Graduate",
    "Some-college": "Collage/Associate Degree",
    "Bachelors": "Bachelor's Degree",
    "Masters": "Advanced Degree",
    "Doctorate": "Advanced Degree",
    "Prof-school": "Advanced Degree",
    "Assoc-acdm": "Assoc-acdm",
    "Assoc-voc": "Assoc-voc",
}

_all_features[FeatureName.EDUCATION_ENCODED] = make_one_hot_encoded(
    AdultData.Column.EDUCATION, _EDUCATION_MAPPING
)

_RELATIONSHIP_MAPPING = {
    "Wife": "Spouse",
    "Husband": "Spouse",
    "Own-Child": "Child",
    "Own-child": "Child",
    "Other-relative": "Other Relative",
    "Not-in-family": "Not family",
    "Unmarried": "Not family",
}

_all_features[FeatureName.RELATIONSHIP_ENCODED] = make_one_hot_encoded(
    AdultData.Column.RELATIONSHIP, _RELATIONSHIP_MAPPING
)


_OCCUPATION_UNKNOWN_DEFAULT = "Unknown"
_OCCUPATION_MAPPING = {
    "Adm-clerical": "White Collar",
    "Armed-Forces": "Military",
    "Craft-repair": "Blue Collar",
    "Exec-managerial": "White Collar",
    "Farming-fishing": "Blue Collar",
    "Handlers-cleaners": "Blue Collar",
    "Machine-op-inspct": "Blue Collar",
    "Other-service": "Service",
    "Priv-house-serv": "Service",
    "Prof-specialty": "White Collar",
    "Protective-service": "Service",
    "Sales": "White Collar",
    "Tech-support": "White Collar",
    "Transport-moving": "Blue Collar",
    "?": _OCCUPATION_UNKNOWN_DEFAULT,
}

_all_features[FeatureName.OCCUPATION_ENCODED] = make_one_hot_encoded(
    AdultData.Column.OCCUPATION,
    mapping_dict=_OCCUPATION_MAPPING,
    unknown_value=_OCCUPATION_UNKNOWN_DEFAULT,
)


_WORK_CLASS_UNKNOWN_DEFAULT = "Unknown"
_WORK_CLASS_MAPPING = {
    "Private": "Private",
    "Self-emp-not-inc": "Self-employed",
    "Self-emp-inc": "Self-employed",
    "Local-gov": "Government",
    "State-gov": "Government",
    "Federal-gov": "Government",
    "Without-pay": "Unemployed",
    "Never-worked": "Unemployed",
    "?": _WORK_CLASS_UNKNOWN_DEFAULT,
}


_all_features[FeatureName.WORK_CLASS_ENCODED] = make_one_hot_encoded(
    AdultData.Column.WORK_CLASS,
    mapping_dict=_WORK_CLASS_MAPPING,
    unknown_value=_WORK_CLASS_UNKNOWN_DEFAULT,
)


_all_features[FeatureName.NET_CAPITAL_STANDARDIZED] = make_pipeline(
    ColumnDifference(
        AdultData.Column.CAPITAL_GAIN,
        AdultData.Column.CAPITAL_LOSS,
        FeatureName.NET_CAPITAL_STANDARDIZED.value,
    ),
    StandardScaler(),
)


_all_features[FeatureName.EDUCATION_NUM_STANDARDIZED] = make_standardized(
    AdultData.Column.EDUCATION_NUM
)
_all_features[FeatureName.HOURS_PER_WEEK_STANDARDIZED] = make_standardized(
    AdultData.Column.HOURS_PER_WEEK
)
_all_features[FeatureName.AGE_STANDARDIZED] = make_standardized(AdultData.Column.AGE)


def collect_features(
    include_only: list[FeatureName] | None = None,
    exclude: list[FeatureName] | None = None,
) -> FeatureUnion:
    feature_list = []
    for identifier, feature in _all_features.items():
        is_include = include_only is None or identifier in include_only
        is_exclude = exclude is not None and identifier in exclude

        if is_include and not is_exclude:
            # we copy to avoid the shared usage of the same object
            feature_list.append(copy(feature))

    return make_union(*feature_list)


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


def select_features(df: pd.DataFrame) -> pd.DataFrame:
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
    return df[selected_features]


def get_income_prediction_features(
    salary_bands: list[int], census_asec_dataset: pd.DataFrame
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

    return census_asec_dataset.pipe(assign_salary_bands, salary_bands).pipe(select_features)
