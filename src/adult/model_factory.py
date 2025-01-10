from typing import Sequence

from sensai.featuregen import FeatureCollector
from sensai.lightgbm import LightGBMVectorClassificationModel
from sensai.sklearn.sklearn_classification import (
    SkLearnRandomForestVectorClassificationModel,
    SkLearnLogisticRegressionVectorClassificationModel,
)
from sensai.xgboost import XGBGradientBoostedVectorClassificationModel

from .data import COLS_FEATURE_CATEGORICAL
from .features import feature_registry, FeatureName, DEFAULT_FEATURES
from .preprocessing import default_preprocessing


class ModelFactory:
    @staticmethod
    def _create_feature_collector(
        features: Sequence[FeatureName] = DEFAULT_FEATURES,
        add_features: Sequence[FeatureName] = (),
    ):
        return FeatureCollector(*features, *add_features, registry=feature_registry)

    @staticmethod
    def _create_name_suffix(add_features: Sequence[FeatureName]) -> str:
        if len(add_features) == 0:
            return ""
        return "_with_" + "_".join([f.value for f in add_features])

    @classmethod
    def create_logistic_regression(
        cls,
        features: Sequence[FeatureName] = DEFAULT_FEATURES,
        add_features: Sequence[FeatureName] = (),
    ):
        fc = cls._create_feature_collector(features, add_features)
        name_suffix = cls._create_name_suffix(add_features)

        return (
            SkLearnLogisticRegressionVectorClassificationModel()
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_feature_transformers(fc.create_feature_transformer_one_hot_encoder())
            .with_name(f"LogisticRegression{name_suffix}")
        )

    @classmethod
    def create_lightgbm(
        cls,
        features: Sequence[FeatureName] = DEFAULT_FEATURES,
        add_features: Sequence[FeatureName] = (),
    ):
        fc = cls._create_feature_collector(features, add_features)
        name_suffix = cls._create_name_suffix(add_features)

        return (
            LightGBMVectorClassificationModel(
                categorical_feature_names=COLS_FEATURE_CATEGORICAL
            )
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_name(f"lightgbm{name_suffix}")
        )

    @classmethod
    def create_xgb(
        cls,
        features: Sequence[FeatureName] = DEFAULT_FEATURES,
        add_features: Sequence[FeatureName] = (),
        min_child_weight: float | None = None,
        **kwargs,
    ):
        fc = cls._create_feature_collector(features, add_features)
        name_suffix = cls._create_name_suffix(add_features)
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
    def create_random_forest(
        cls,
        features: Sequence[FeatureName] = DEFAULT_FEATURES,
        add_features: Sequence[FeatureName] = (),
    ):
        fc = cls._create_feature_collector(features, add_features)
        name_suffix = cls._create_name_suffix(add_features)

        return (
            SkLearnRandomForestVectorClassificationModel()
            .with_raw_input_transformers(default_preprocessing)
            .with_feature_collector(fc)
            .with_feature_transformers(fc.create_feature_transformer_one_hot_encoder())
            .with_name(f"RandomForest{name_suffix}")
        )
