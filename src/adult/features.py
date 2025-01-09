from enum import Enum

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
    COLS_FEATURE_CATEGORICAL,
    COLS_FEATURE_NUMERIC,
    COL_CAPITAL_GAIN,
    COL_CAPITAL_LOSS, COL_WORKCLASS, COL_OCCUPATION,
)


class FeatureName(Enum):
    CATEGORICAL = "categorical"
    NUMERICAL = "numerical"
    NET_CAPITAL = "net-capital"
    WORK_CLASS = COL_WORKCLASS
    OCCUPATION = COL_OCCUPATION


class NetCapital(RuleBasedFeatureGenerator):
    COL_NET_CAPITAL = "net-capital"

    def _generate(self, df: pd.DataFrame, ctx=None) -> pd.DataFrame:
        values = df[COL_CAPITAL_GAIN] - df[COL_CAPITAL_LOSS]
        return pd.DataFrame({self.COL_NET_CAPITAL: values}, index=df.index)


feature_registry = FeatureGeneratorRegistry()

feature_registry.register_factory(
    FeatureName.NET_CAPITAL,
    lambda: NetCapital(
        normalisation_rule_template=DFTNormalisation.RuleTemplate(
            transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
        )
    ),
)

feature_registry.register_factory(
    FeatureName.WORK_CLASS,
    lambda: FeatureGeneratorTakeColumns(
        COL_WORKCLASS, categorical_feature_names=COLS_FEATURE_CATEGORICAL
    ),
)

feature_registry.register_factory(
    FeatureName.OCCUPATION,
    lambda: FeatureGeneratorTakeColumns(
        COL_OCCUPATION, categorical_feature_names=COLS_FEATURE_CATEGORICAL
    ),
)

feature_registry.register_factory(
    FeatureName.CATEGORICAL,
    lambda: FeatureGeneratorTakeColumns(
        COLS_FEATURE_CATEGORICAL, categorical_feature_names=COLS_FEATURE_CATEGORICAL
    ),
)
feature_registry.register_factory(
    FeatureName.NUMERICAL,
    lambda: FeatureGeneratorTakeColumns(
        COLS_FEATURE_NUMERIC,
        normalisation_rule_template=DFTNormalisation.RuleTemplate(
            transformer_factory=SkLearnTransformerFactoryFactory.StandardScaler()
        ),
    ),
)
