from sensai.featuregen import FeatureCollector
from sensai.lightgbm import LightGBMVectorClassificationModel
from sensai.sklearn.sklearn_classification import (
    SkLearnRandomForestVectorClassificationModel,
    SkLearnLogisticRegressionVectorClassificationModel,
)
from sensai.data_transformation import DFTDropNA
from sensai.xgboost import XGBGradientBoostedVectorClassificationModel

from .data import COLS_FEATURE_CATEGORICAL
from .features import feature_registry, FeatureName
from .preprocessing import default_preprocessing, WorkClassMapping


class ModelFactory:
    DEFAULT_FEATURES = (FeatureName.NUMERICAL, FeatureName.CATEGORICAL, FeatureName.NET_CAPITAL)

    @classmethod
    def create_lightgbm(cls):
        fc = FeatureCollector(*cls.DEFAULT_FEATURES, registry=feature_registry)
        return (
            LightGBMVectorClassificationModel(
                categorical_feature_names=COLS_FEATURE_CATEGORICAL
            )
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_name(f"lightgbm")
        )

    @classmethod
    def create_logistic_regression(cls):
        fc = FeatureCollector(*cls.DEFAULT_FEATURES, registry=feature_registry)
        return (
            SkLearnLogisticRegressionVectorClassificationModel(
                solver="lbfgs", max_iter=10000
            )
            .with_feature_collector(fc)
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_transformers(fc.create_feature_transformer_one_hot_encoder())
            .with_name("LogisticRegression-orig")
        )

    @classmethod
    def create_xgb(
        cls, name_suffix="", min_child_weight: float | None = None, **kwargs
    ):
        fc = FeatureCollector(*cls.DEFAULT_FEATURES, registry=feature_registry)
        return (
            XGBGradientBoostedVectorClassificationModel(
                min_child_weight=min_child_weight,
                **kwargs,
            )
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_feature_transformers(fc.create_feature_transformer_one_hot_encoder())
            .with_name(f"XGBoost{name_suffix}")
        )

    @classmethod
    def create_random_forest(cls):
        fc = FeatureCollector(*cls.DEFAULT_FEATURES, registry=feature_registry)
        return (
            SkLearnRandomForestVectorClassificationModel()
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_feature_transformers(fc.create_feature_transformer_one_hot_encoder())
            .with_name(f"RandomForest")
        )
