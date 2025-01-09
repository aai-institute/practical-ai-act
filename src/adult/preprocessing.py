from typing import Any

import pandas as pd
from sensai.data_transformation import RuleBasedDataFrameTransformer

from adult.data import COL_MARITAL_STATUS, COL_WORKCLASS, COL_EDUCATION, COL_OCCUPATION, \
    COL_RELATIONSHIP, COL_RACE, COL_NATIVE_COUNTRY


class DFTFillNA(RuleBasedDataFrameTransformer):
    def __init__(self, fill_value: Any, column_subset: list[str] | str | None = None):
        self.fill_value = fill_value
        self.column_subset = column_subset
        super().__init__()

    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.column_subset:
            df.loc[:, self.column_subset] = df[self.column_subset].fillna(self.fill_value)
        else:
            df.fillna(self.fill_value, inplace=True)
        return df


class ColumnValueMapping(RuleBasedDataFrameTransformer):
    """
    Maps values in a column according to a mapping dictionary

    Args:
        column: The column to apply the mapping to
        mapping: A dictionary mapping the original values to the new values
    """
    def __init__(self, column: str, mapping: dict, fill_value: Any | None = None):
        self.fill_value = fill_value
        self.column = column
        self.mapping = mapping
        super().__init__()

    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df.loc[:, self.column] = df[self.column].map(lambda x: self.mapping.get(x, x))
        if self.fill_value:
            df.loc[:, self.column] = df[self.column].fillna(self.fill_value)
        return df


class WorkClassMapping(ColumnValueMapping):
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

    def __init__(self, fill_na: bool = False):
        super().__init__(COL_WORKCLASS, self.WORKCLASS_MAPPING, fill_value=self.UNKNOWN_DEFAULT if fill_na else None)

class EducationMapping(ColumnValueMapping):
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
        super().__init__(COL_EDUCATION, self.EDUCATION_MAPPING)


class MaritalStatusMapping(ColumnValueMapping):
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
        super().__init__(COL_MARITAL_STATUS, self.MARITAL_STATUS_MAPPING)


class OccupationMapping(ColumnValueMapping):

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

    def __init__(self, fill_na: bool = False):
        super().__init__(COL_OCCUPATION, self.OCCUPATION_MAPPING, fill_value=self.UNKNOWN_DEFAULT if fill_na else None)




class RelationShipMapping(ColumnValueMapping):
    RELATIONSHIP_MAPPING = {
        "Wife": "Spouse",
        "Husband": "Spouse",
        "Own-Child": "Child",
        "Other-relative": "Other Relative",
        "Not-in-family": "Not family",
        "Unmarried": "Not family",
    }

    def __init__(self):
        super().__init__(COL_RELATIONSHIP, self.RELATIONSHIP_MAPPING)


class RaceMapping(ColumnValueMapping):
    RACE_MAPPING = {
        "White": "White",
        "Black": "Other",
        "Asian-Pac-Islander": "Other",
        "Amer-Indian-Eskimo": "Other",
        "Other": "Other",
    }

    def __init__(self):
        super().__init__(COL_RACE, self.RACE_MAPPING)


class NativeCountryMapping(ColumnValueMapping):

    UNKNOWN_DEFAULT = "Unknown"
    OTHER_DEFAULT = "Other"
    COUNTRY_MAPPING = {"United-States": "US", "?": UNKNOWN_DEFAULT, "US": "US"}

    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        def reduce_native_country(country):
            if country == "United-States":
                return "US"
            elif country == "?":
                return self.UNKNOWN_DEFAULT
            else:
                return "Other"

        df.loc[:, COL_NATIVE_COUNTRY] = df[COL_NATIVE_COUNTRY].apply(reduce_native_country)
        return df



default_preprocessing = [
    WorkClassMapping(),
    DFTFillNA(fill_value=WorkClassMapping.UNKNOWN_DEFAULT, column_subset=COL_WORKCLASS),
    EducationMapping(),
    MaritalStatusMapping(),
    OccupationMapping(),
    DFTFillNA(fill_value=OccupationMapping.UNKNOWN_DEFAULT, column_subset=COL_OCCUPATION),
    RelationShipMapping(),
    RaceMapping(),
    #NativeCountryMapping(),
    DFTFillNA(fill_value=NativeCountryMapping.UNKNOWN_DEFAULT, column_subset=COL_NATIVE_COUNTRY),
]
