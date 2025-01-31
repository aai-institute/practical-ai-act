"""Data and model pipeline for the CPS ASEC income predictor."""

import typing
from typing import Any, Protocol

import mlflow
import pandas as pd
import sklearn.pipeline
from functools import partial
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin

from adult.data import AdultData, AdultASECData
from adult.preprocessing import WorkClassMapping, EducationMapping
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder



if typing.TYPE_CHECKING:
    # Work around lazy imports in mlflow main module
    import mlflow.sklearn


# TODO: Adjust to actual paths in code.
CONFIG = {
    "paths": {
        "raw_data": "data/raw/",
        "clean_data": "data/clean/",
        "model": "models/",
    },
    "mlflow": {
        "tracking_uri": "http://localhost:5000",
        "experiment_name": "cps_asec",
    },
}


def setup_mlflow():
    mlflow.set_tracking_uri(CONFIG["mlflow"]["tracking_uri"])
    mlflow.set_experiment("cps_asec")
    mlflow.sklearn.autolog()




class NAFiller(ColumnTransformer):
    def __init__(self, columns: str | list[str], fill_value: typing.Any):
        super().__init__(
            [
                (
                    f"{columns}_fill_na",
                    SimpleImputer(strategy="constant", fill_value=fill_value),
                    columns,
                )
            ],
            remainder="keep",
        )

class ColumnMap(BaseEstimator, TransformerMixin):
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
        X.loc[:, self.column] = X[self.column].map(
            lambda x: self.mapping_dict.get(x, x)
        )
        return X


class NativeCountryMapping(ColumnTransformer):
    UNKNOWN_DEFAULT = "Unknown"
    OTHER_DEFAULT = "Other"
    COUNTRY_MAPPING = {"United-States": "US", "?": UNKNOWN_DEFAULT}

    def __init__(self):
        # TODO (nicholasjng): This is hacky, please improve.
        def _transform(df):
            def reduce_native_country(country):
                if country in {self.UNKNOWN_DEFAULT, self.OTHER_DEFAULT, "US"}:
                    return country

                return self.COUNTRY_MAPPING.get(country, self.OTHER_DEFAULT)

            df.loc[:, AdultData.Column.NATIVE_COUNTRY] = df[
                AdultData.Column.NATIVE_COUNTRY
            ].apply(reduce_native_country)

        super().__init__(
            [("native_country", _transform, "native_country")], remainder="keep"
        )


class WorkClassMapping(ColumnMap):
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
        super().__init__(
            AdultASECData.Column.WORKER_CLASS.value, self.WORKCLASS_MAPPING
        )


class OccupationMapping(ColumnMap):
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
        super().__init__(
            AdultData.Column.EDUCATION,
            self.OCCUPATION_MAPPING,
        )


class EducationMapping(ColumnMap):
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
        super().__init__(AdultData.Column.EDUCATION, self.EDUCATION_MAPPING)


class MaritalStatusMapping(ColumnMap):
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
        super().__init__(AdultData.Column.MARITAL_STATUS, self.MARITAL_STATUS_MAPPING)


class RelationShipMapping(ColumnMap):
    RELATIONSHIP_MAPPING = {
        "Wife": "Spouse",
        "Husband": "Spouse",
        "Own-Child": "Child",
        "Other-relative": "Other Relative",
        "Not-in-family": "Not family",
        "Unmarried": "Not family",
    }

    def __init__(self):
        super().__init__(AdultData.Column.RELATIONSHIP, self.RELATIONSHIP_MAPPING)


class RaceMapping(ColumnMap):
    RACE_MAPPING = {
        "White": "White",
        "Black": "Other",
        "Asian-Pac-Islander": "Other",
        "Amer-Indian-Eskimo": "Other",
        "Other": "Other",
    }

    def __init__(self):
        super().__init__(AdultData.Column.RACE, self.RACE_MAPPING)


def cps_asec_model():
    p = sklearn.pipeline.Pipeline(
        [
            (str(WorkClassMapping), WorkClassMapping()),
            # NAFiller(
            #    columns=AdultData.Column.WORK_CLASS,
            #    fill_value=WorkClassMapping.UNKNOWN_DEFAULT,
            # ),
            # EducationMapping(),
            # MaritalStatusMapping(),
            # OccupationMapping(),
            # NAFiller(
            #    columns=AdultData.Column.OCCUPATION,
            #    fill_value=OccupationMapping.UNKNOWN_DEFAULT,
            # ),
            # RelationShipMapping(),
            # RaceMapping(),
            # NativeCountryMapping(),
            # NAFiller(
            #    columns=AdultData.Column.NATIVE_COUNTRY,
            #    fill_value=NativeCountryMapping.UNKNOWN_DEFAULT,
            # ),
        ]
    )
    # TODO(nicholasjng): Add model / other steps.
    return p


