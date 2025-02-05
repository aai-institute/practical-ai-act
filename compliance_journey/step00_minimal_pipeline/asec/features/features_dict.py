from typing import Hashable, Callable, Literal, get_args

from sklearn.pipeline import make_pipeline, FeatureUnion, make_union, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from adult.data import AdultData
from asec.features.base import TakeColumn, MappedColumn, ColumnDifference, Feature


_features_factory_dict: dict[Hashable, Callable[[], Feature | Pipeline]] = {}


def collect_features(
    include_only: list[Hashable] | None = None,
    exclude: list[Hashable] | None = None,
) -> FeatureUnion:
    feature_list = []
    for identifier, factory in _features_factory_dict.items():
        is_include = include_only is None or identifier in include_only
        is_exclude = exclude is not None and identifier in exclude

        if is_include and not is_exclude:
           feature_list.append(factory())

    return make_union(*feature_list)


_features_factory_dict[AdultData.Column.SEX] = lambda: make_pipeline(
    TakeColumn(AdultData.Column.SEX.value),
    OneHotEncoder(categories=[["Female", "Male"]]),
)

_RACE_MAPPING = {
    "White": "White",
    "Black": "Other",
    "Asian-Pac-Islander": "Other",
    "Amer-Indian-Eskimo": "Other",
    "Other": "Other",
}

_features_factory_dict[AdultData.Column.RACE] = lambda: make_pipeline(
    MappedColumn(AdultData.Column.RACE.value, _RACE_MAPPING),
    OneHotEncoder(categories=[list(set(_RACE_MAPPING.values()))]),
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

_features_factory_dict[AdultData.Column.MARITAL_STATUS] = lambda: make_pipeline(
    MappedColumn(AdultData.Column.MARITAL_STATUS.value, _MARITAL_STATUS_MAPPING),
    OneHotEncoder(categories=[list(set(_MARITAL_STATUS_MAPPING.values()))]),
)


_COUNTRY_MAPPING = {"United-States": "US", "?": "Unknown"}
_OTHER_COUNTRY_DEFAULT = "Other"


_features_factory_dict[AdultData.Column.NATIVE_COUNTRY] = lambda: make_pipeline(
    MappedColumn(
        AdultData.Column.NATIVE_COUNTRY,
        _COUNTRY_MAPPING,
        unknown_default=_OTHER_COUNTRY_DEFAULT,
    ),
    OneHotEncoder(
        categories=[
            list(set(_COUNTRY_MAPPING.values()).union({_OTHER_COUNTRY_DEFAULT}))
        ]
    ),
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


_features_factory_dict[AdultData.Column.EDUCATION] = lambda: make_pipeline(
    MappedColumn(AdultData.Column.EDUCATION.value, _EDUCATION_MAPPING),
    OneHotEncoder(categories=[list(set(_EDUCATION_MAPPING.values()))]),
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

_features_factory_dict[AdultData.Column.RELATIONSHIP] = lambda: make_pipeline(
    MappedColumn(AdultData.Column.RELATIONSHIP.value, _RELATIONSHIP_MAPPING),
    OneHotEncoder(categories=[list(set(_RELATIONSHIP_MAPPING.values()))]),
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

_features_factory_dict[AdultData.Column.OCCUPATION] = lambda: make_pipeline(
    MappedColumn(
        AdultData.Column.OCCUPATION.value,
        _OCCUPATION_MAPPING,
        unknown_default=_OCCUPATION_UNKNOWN_DEFAULT,
    ),
    OneHotEncoder(categories=[list(set(_OCCUPATION_MAPPING.values()))]),
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

_features_factory_dict[AdultData.Column.WORK_CLASS] = lambda: make_pipeline(
    MappedColumn(
        AdultData.Column.WORK_CLASS.value,
        _WORK_CLASS_MAPPING,
        unknown_default=_WORK_CLASS_UNKNOWN_DEFAULT,
    ),
    OneHotEncoder(categories=[list(set(_WORK_CLASS_MAPPING.values()))]),
)

NET_CAPITAL_FEATURE = Literal["net-capital"]

_features_factory_dict[NET_CAPITAL_FEATURE] = lambda: make_pipeline(
    ColumnDifference(
        AdultData.Column.CAPITAL_GAIN,
        AdultData.Column.CAPITAL_LOSS,
        get_args(NET_CAPITAL_FEATURE)[0],
    ),
    StandardScaler(),
)

for col in AdultData.COLS_NUMERIC:
    _features_factory_dict[col] = lambda: make_pipeline(
        TakeColumn(col.value), StandardScaler()
    )
