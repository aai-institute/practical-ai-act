from enum import Enum

from sensai.data_transformation import DFTNormalisation, \
    SkLearnTransformerFactoryFactory
from sensai.featuregen import FeatureGeneratorRegistry, FeatureGeneratorTakeColumns

from statlog.data import COLS_FEATURE_CATEGORICAL, COLS_FEATURE_NUMERIC


class FeatureName(Enum):
    CATEGORICAL = "categorical"
    NUMERICAL = "numerical"


feature_registry = FeatureGeneratorRegistry()


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