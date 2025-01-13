from __future__ import annotations
from enum import Enum
from functools import partial
from typing import Union, Sequence

import numpy as np
import pandas as pd
from sensai.data_transformation import (
    DFTNormalisation,
    SkLearnTransformerFactoryFactory,
)
from sensai.featuregen import (
    FeatureGeneratorRegistry,
    FeatureGeneratorTakeColumns,
)
from sensai.columngen import ColumnGenerator

from adult.data import AdultData


class AdultFeatureRegistry(FeatureGeneratorRegistry):
    class FeatureName(Enum):
        NET_CAPITAL = "net-capital"
        WORK_CLASS = AdultData.Column.WORK_CLASS
        OCCUPATION = AdultData.Column.OCCUPATION
        RACE = AdultData.Column.RACE
        SEX = AdultData.Column.SEX
        AGE = AdultData.Column.AGE
        RELATIONSHIP = AdultData.Column.RELATIONSHIP
        NATIVE_COUNTRY = AdultData.Column.NATIVE_COUNTRY
        MARITAL_STATUS = AdultData.Column.MARITAL_STATUS
        EDUCATION = AdultData.Column.EDUCATION
        EDUCATION_NUM = AdultData.Column.EDUCATION_NUM
        HOURS_PER_WEEK = AdultData.Column.HOURS_PER_WEEK

        @staticmethod
        def personal_features() -> Sequence[AdultFeatureRegistry.FeatureName]:
            return (
                AdultFeatureRegistry.FeatureName.SEX,
                AdultFeatureRegistry.FeatureName.AGE,
                AdultFeatureRegistry.FeatureName.RACE,
                AdultFeatureRegistry.FeatureName.MARITAL_STATUS,
                AdultFeatureRegistry.FeatureName.NATIVE_COUNTRY,
                AdultFeatureRegistry.FeatureName.RELATIONSHIP,
            )

        @classmethod
        def default_features(cls) -> Sequence[AdultFeatureRegistry.FeatureName]:
            return tuple(
                [
                    feat
                    for feat in AdultFeatureRegistry.FeatureName
                    if feat not in cls.personal_features()
                ]
            )

    def __init__(self):
        super().__init__()
        self._register_column_features()

    @staticmethod
    def _is_categorical_column(member: AdultFeatureRegistry.FeatureName):
        cat_cols = [m.value for m in AdultData.COLS_CATEGORICAL]
        return member.value in cat_cols

    @staticmethod
    def _is_numeric_column(member: AdultFeatureRegistry.FeatureName):
        num_cols = [m.value for m in AdultData.COLS_NUMERIC]
        return member.value in num_cols

    def _register_column_features(self):
        for member in self.FeatureName:
            if self._is_categorical_column(member):
                self.register_categorical(AdultData.Column(member.value).value)
            elif self._is_numeric_column(member):
                self.register_standard_scaled(AdultData.Column(member.value).value)

    def register_standard_scaled(self, col_name: str):
        self.register_factory(
            self.FeatureName(col_name),
            partial(
                FeatureGeneratorTakeColumns,
                col_name,
                normalisation_rule_template=DFTNormalisation.RuleTemplate(
                    transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
                ),
            ),
        )

    def register_min_max_scaled(self, col_name: str):
        self.register_factory(
            self.FeatureName(col_name),
            partial(
                FeatureGeneratorTakeColumns,
                col_name,
                normalisation_rule_template=DFTNormalisation.RuleTemplate(
                    transformer_factory=SkLearnTransformerFactoryFactory.MinMaxScaler()
                ),
            ),
        )

    def register_categorical(self, col_name: str):
        self.register_factory(
            self.FeatureName(col_name),
            partial(
                FeatureGeneratorTakeColumns,
                col_name,
                categorical_feature_names=col_name,
            ),
        )


class _NetCapital(ColumnGenerator):
    def __init__(self):
        super().__init__(AdultFeatureRegistry.FeatureName.NET_CAPITAL.value)

    def _generate_column(self, df: pd.DataFrame) -> Union[pd.Series, list, np.ndarray]:
        return df[AdultData.Column.CAPITAL_GAIN] - df[AdultData.Column.CAPITAL_LOSS]


adult_feature_registry = AdultFeatureRegistry()

adult_feature_registry.register_factory(
    AdultFeatureRegistry.FeatureName.NET_CAPITAL,
    lambda: _NetCapital().to_feature_generator(
        normalisation_rule_template=DFTNormalisation.RuleTemplate(
            transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
        ),
    ),
)
