from typing import Any, Protocol, cast, Literal

from numpy.random.mtrand import Sequence
from sklearn.pipeline import make_pipeline, make_union, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import (
    StandardScaler,
    OrdinalEncoder,
    OneHotEncoder,
    FunctionTransformer,
)
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


import pandas as pd

from .data import AdultData


class Feature(Protocol):
    def fit(self, X, y=None) -> None: ...

    def transform(self, X): ...


class TakeColumn(BaseEstimator, TransformerMixin):
    def __init__(self, column: str):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[[self.column]]


class _ExtendedFeature(Pipeline):
    def __init__(
        self,
        column_or_feature: str | Feature,
        extensions: Sequence[Any],
    ):
        if isinstance(column_or_feature, str):
            base_trafo = TakeColumn(column_or_feature)
        else:
            base_trafo = column_or_feature

        trafo_list = [(str(TakeColumn), base_trafo)]
        trafo_list.extend([(str(extension), extension) for extension in extensions])

        # this has to be here, due to implementation of sklearn Pipeline
        self.column_or_feature = column_or_feature
        super().__init__(trafo_list)


class OrdinalEncoded(_ExtendedFeature):
    def __init__(
        self,
        column_or_feature: str | Feature,
        categories: list[Any] | Literal["auto"] = "auto",
    ):
        self.categories = categories
        super().__init__(column_or_feature, [OrdinalEncoder(categories=categories)])


class OneHotEncoded(_ExtendedFeature):
    def __init__(
        self,
        column_or_feature: str | Feature,
        categories: list[Any] | Literal["auto"] = "auto",
    ):
        self.categories = categories
        super().__init__(column_or_feature, [OneHotEncoder(categories=categories)])


class StandardScaled(_ExtendedFeature):
    def __init__(self, column_or_feature: str | Feature):
        super().__init__(column_or_feature, [StandardScaler()])


class MappedColumn(BaseEstimator, TransformerMixin):
    def __init__(self, column: str, mapping_dict: dict[str, Any]):
        """
        Parameters:
        - column: str, the column to map
        - mapping_dict: dict, the dictionary with mapping values
        """
        self.column = column
        self.mapping_dict = mapping_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[self.column].map(self.mapping_dict).to_frame()


class WorkClass(OneHotEncoded):
    UNKNOWN_DEFAULT = "Unknown"
    WORKCLASS_MAPPING = {
        "Private": "Private",
        "Self-emp-not-inc": "Self-employed",
        "Self-emp-inc": "Self-employed",
        "Local-gov": "Government",
        "State-gov": "Government",
        "Federal-gov": "Government",
        "Without-pay": "Unemployed",
        "Never-worked": "Unemployed",
        "?": UNKNOWN_DEFAULT,
    }

    def __init__(self):
        mapped_column = MappedColumn(
            AdultData.Column.WORK_CLASS, self.WORKCLASS_MAPPING
        )
        base = make_pipeline(
            mapped_column,
            SimpleImputer(strategy="constant", fill_value=self.UNKNOWN_DEFAULT),
        )
        super().__init__(
            cast(Feature, base), categories=[list(set(self.WORKCLASS_MAPPING.values()))]
        )


class Occupation(OneHotEncoded):
    UNKNOWN_DEFAULT = "Unknown"
    OCCUPATION_MAPPING = {
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
        "?": UNKNOWN_DEFAULT,
    }

    def __init__(self):
        mapped_column = MappedColumn(
            AdultData.Column.OCCUPATION, self.OCCUPATION_MAPPING
        )
        base = make_pipeline(
            mapped_column,
            SimpleImputer(strategy="constant", fill_value=self.UNKNOWN_DEFAULT),
        )
        super().__init__(
            cast(Feature, base),
            categories=[list(set(self.OCCUPATION_MAPPING.values()))],
        )


class Race(OneHotEncoded):
    RACE_MAPPING = {
        "White": "White",
        "Black": "Other",
        "Asian-Pac-Islander": "Other",
        "Amer-Indian-Eskimo": "Other",
        "Other": "Other",
    }

    def __init__(self):
        mapped_column = MappedColumn(AdultData.Column.RACE, self.RACE_MAPPING)
        super().__init__(
            cast(Feature, mapped_column),
            categories=[list(set(self.RACE_MAPPING.values()))],
        )


class RelationShip(OneHotEncoded):
    RELATIONSHIP_MAPPING = {
        "Wife": "Spouse",
        "Husband": "Spouse",
        "Own-Child": "Child",
        "Own-child": "Child",
        "Other-relative": "Other Relative",
        "Not-in-family": "Not family",
        "Unmarried": "Not family",
    }

    def __init__(self):
        mapped_column = MappedColumn(
            AdultData.Column.RELATIONSHIP, self.RELATIONSHIP_MAPPING
        )
        super().__init__(
            cast(Feature, mapped_column),
            categories=[list(set(self.RELATIONSHIP_MAPPING.values()))],
        )


class MaritalStatus(OneHotEncoded):
    MARITAL_STATUS_MAPPING = {
        "Married-civ-spouse": "Married",
        "Married-spouse-absent": "Married",
        "Married-AF-spouse": "Married",
        "Never-married": "Never Married",
        "Divorced": "Previously Married",
        "Separated": "Previously Married",
        "Widowed": "Previously Married",
    }

    def __init__(self):
        mapped_column = MappedColumn(
            AdultData.Column.MARITAL_STATUS, self.MARITAL_STATUS_MAPPING
        )
        super().__init__(
            cast(Feature, mapped_column),
            categories=[list(set(self.MARITAL_STATUS_MAPPING.values()))],
        )


class Education(OneHotEncoded):
    EDUCATION_MAPPING = {
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

    def __init__(self):
        mapped_column = MappedColumn(AdultData.Column.EDUCATION, self.EDUCATION_MAPPING)
        super().__init__(
            cast(Feature, mapped_column),
            categories=[list(set(self.EDUCATION_MAPPING.values()))],
        )


class NativeCountry(OneHotEncoded):
    UNKNOWN_DEFAULT = "Unknown"
    OTHER_DEFAULT = "Other"
    COUNTRY_MAPPING = {"United-States": "US", "?": UNKNOWN_DEFAULT}

    def __init__(self):

        def reduce_native_country(country) -> str:
            if country in {self.UNKNOWN_DEFAULT, self.OTHER_DEFAULT, "US"}:
                return country

            return self.COUNTRY_MAPPING.get(country, self.OTHER_DEFAULT)

        def frame_map(df: pd.DataFrame) -> pd.DataFrame:
            df.loc[:, AdultData.Column.NATIVE_COUNTRY] = df[AdultData.Column.NATIVE_COUNTRY].apply(reduce_native_country)
            return df


        base = make_pipeline(
            TakeColumn(AdultData.Column.NATIVE_COUNTRY),
            ColumnTransformer([("mapping", FunctionTransformer(frame_map), [AdultData.Column.NATIVE_COUNTRY.value])]),
            SimpleImputer(strategy="constant", fill_value=self.UNKNOWN_DEFAULT),
        )
        categories = {
            self.UNKNOWN_DEFAULT,
            self.OTHER_DEFAULT,
            *self.COUNTRY_MAPPING.values(),
        }
        super().__init__(cast(Feature, base), categories=[list(set(categories))])


mapped_features = [
    RelationShip(),
    WorkClass(),
    Education(),
    Occupation(),
    Race(),
    MaritalStatus(),
    NativeCountry(),
]

numerical_features = [StandardScaled(col.value) for col in AdultData.COLS_NUMERIC]


default_preprocessing = make_union(
    OneHotEncoded(AdultData.Column.SEX.value),
    *mapped_features,
    *numerical_features,
)
