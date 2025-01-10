from __future__ import annotations
from enum import Enum
from functools import partial

import pandas as pd
from sensai.data_transformation import (
    DFTNormalisation,
    SkLearnTransformerFactoryFactory,
)
from sensai.featuregen import (
    FeatureGeneratorRegistry,
    FeatureGeneratorTakeColumns,
    RuleBasedFeatureGenerator,
)

from adult.data import (
    COL_CAPITAL_GAIN,
    COL_CAPITAL_LOSS,
    COL_WORKCLASS,
    COL_OCCUPATION,
    COL_RACE,
    COL_SEX,
    COL_AGE,
    COL_RELATIONSHIP,
    COL_NATIVE_COUNTRY,
    COL_MARITAL_STATUS,
    COL_EDUCATION,
    COL_EDUCATION_NUM,
    COL_HOURS_PER_WEEK,
)


class FeatureName(Enum):
    NET_CAPITAL = "net-capital"
    WORK_CLASS = COL_WORKCLASS
    OCCUPATION = COL_OCCUPATION
    RACE = COL_RACE
    SEX = COL_SEX
    AGE = COL_AGE
    RELATIONSHIP = COL_RELATIONSHIP
    NATIVE_COUNTRY = COL_NATIVE_COUNTRY
    MARITAL_STATUS = COL_MARITAL_STATUS
    EDUCATION = COL_EDUCATION
    EDUCATION_NUM = COL_EDUCATION_NUM
    HOURS_PER_WEEK = COL_HOURS_PER_WEEK

    @classmethod
    def standard_scaled_feature(cls, col_name: "FeatureName"):
        return partial(
            FeatureGeneratorTakeColumns,
            col_name,
            normalisation_rule_template=DFTNormalisation.RuleTemplate(
                transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
            ),
        )

    @classmethod
    def min_max_scaled_feature(cls, col_name: "FeatureName"):
        return partial(
            FeatureGeneratorTakeColumns,
            col_name,
            normalisation_rule_template=DFTNormalisation.RuleTemplate(
                transformer_factory=SkLearnTransformerFactoryFactory.MinMaxScaler()
            ),
        )

    @classmethod
    def categorical_feature(cls, col_name: "FeatureName"):
        return partial(
            FeatureGeneratorTakeColumns,
            col_name,
            categorical_feature_names=col_name,
        )


class NetCapital(RuleBasedFeatureGenerator):
    COL_NET_CAPITAL = "net-capital"

    def _generate(self, df: pd.DataFrame, ctx=None) -> pd.DataFrame:
        values = df[COL_CAPITAL_GAIN] - df[COL_CAPITAL_LOSS]
        return pd.DataFrame({self.COL_NET_CAPITAL: values}, index=df.index)


feature_registry = FeatureGeneratorRegistry()

feature_registry.register_factory(
    FeatureName.RACE, FeatureName.categorical_feature(COL_RACE)
)

feature_registry.register_factory(
    FeatureName.SEX, FeatureName.categorical_feature(COL_SEX)
)

feature_registry.register_factory(
    FeatureName.NET_CAPITAL,
    partial(
        NetCapital,
        normalisation_rule_template=DFTNormalisation.RuleTemplate(
            transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
        ),
    ),
)

feature_registry.register_factory(
    FeatureName.WORK_CLASS,
    FeatureName.categorical_feature(COL_WORKCLASS),
)

feature_registry.register_factory(
    FeatureName.OCCUPATION,
    FeatureName.categorical_feature(COL_OCCUPATION),
)

feature_registry.register_factory(
    FeatureName.AGE,
    FeatureName.standard_scaled_feature(COL_AGE),
)

feature_registry.register_factory(
    FeatureName.RELATIONSHIP,
    FeatureName.categorical_feature(COL_RELATIONSHIP),
)

feature_registry.register_factory(
    FeatureName.NATIVE_COUNTRY,
    FeatureName.categorical_feature(COL_NATIVE_COUNTRY),
)

feature_registry.register_factory(
    FeatureName.MARITAL_STATUS,
    FeatureName.categorical_feature(COL_MARITAL_STATUS),
)

feature_registry.register_factory(
    FeatureName.EDUCATION,
    FeatureName.categorical_feature(COL_EDUCATION),
)

feature_registry.register_factory(
    FeatureName.EDUCATION_NUM,
    FeatureName.standard_scaled_feature(COL_EDUCATION_NUM),
)

feature_registry.register_factory(
    FeatureName.HOURS_PER_WEEK,
    FeatureName.standard_scaled_feature(COL_HOURS_PER_WEEK),
)
PERSONAL_FEATURES = (
    FeatureName.SEX,
    FeatureName.AGE,
    FeatureName.RACE,
    FeatureName.MARITAL_STATUS,
    FeatureName.NATIVE_COUNTRY,
    FeatureName.RELATIONSHIP,
)

DEFAULT_FEATURES = tuple(
    [feat for feat in FeatureName if feat not in PERSONAL_FEATURES]
)
