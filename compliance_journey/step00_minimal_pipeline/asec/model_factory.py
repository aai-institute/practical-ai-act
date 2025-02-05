from sklearn.pipeline import make_pipeline, Pipeline, make_union
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from .features import collect_features, FeatureName

class ModelFactory:
    @classmethod
    def create_xgb(
        cls,
        include_only: list[FeatureName] | None = None,
        exclude: list[FeatureName] | None = None,
        add: list[Pipeline | ColumnTransformer] | None = None,
        **xgb_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        return make_pipeline(feature_union, XGBClassifier(**xgb_kwargs))

    @classmethod
    def create_lightgbm(
            cls,
            include_only: list[FeatureName] | None = None,
            exclude: list[FeatureName] | None = None,
            add: list[Pipeline | ColumnTransformer] | None = None,
            **lgbm_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        return make_pipeline(feature_union, LGBMClassifier(**lgbm_kwargs))

    @classmethod
    def create_mlp(
            cls,
            include_only: list[FeatureName] | None = None,
            exclude: list[FeatureName] | None = None,
            add: list[Pipeline | ColumnTransformer] | None = None,
            **mlp_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        return make_pipeline(feature_union, MLPClassifier(**mlp_kwargs))

    @classmethod
    def _create_feature_union(
        cls,
        include_only: list[FeatureName] | None = None,
        exclude: list[FeatureName] | None = None,
        add: list[Pipeline | ColumnTransformer] | None = None,
    ):
        feature_union = collect_features(
            include_only=include_only,
            exclude=exclude,
        )
        if add is not None:
            feature_union = make_union(*feature_union.transformer_list, *add)
        return feature_union
