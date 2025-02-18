from typing import Any

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import make_pipeline, Pipeline, make_union
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.utils.metaestimators import available_if
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, \
    OrdinalEncoder

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from .data import CensusASECMetadata
from .features import collect_features, FeatureName


class LabelEncodedClassifier(ClassifierMixin, BaseEstimator):
    """
    A simple wrapper for a given classifier that automatically encodes target labels
    before fitting and decodes predictions. There is an ongoing
    [issue](https://github.com/scikit-learn/scikit-learn/pull/29952)
    at the sklearn repository and a
    [preliminary implementation](https://github.com/gtauzin/scikit-learn/blob/transformed_target_clf/sklearn/compose/_target.py)

    Attributes:
        classifier (ClassifierMixin): The base classifier.
        encoder (LabelEncoder): The encoder for transforming target labels.
    """

    def __init__(self, classifier, encoder: LabelEncoder):
        self.classifier = classifier
        self.encoder = encoder

    def fit(self, X, y, **params):
        self.classifier.fit(X, self.encoder.fit_transform(y), **params)

    def predict(self, X, **params):
        pred = self.classifier.predict(X, **params)
        return self.encoder.inverse_transform(pred)

    @available_if(lambda self: hasattr(self.classifier, "predict_proba"))
    def predict_proba(self, X, **params):
        return self.classifier.predict_proba(X, **params)

    @available_if(lambda self: hasattr(self.classifier, "predict_log_proba"))
    def predict_log_proba(self, X, **params):
        return self.classifier.predict_proba(X, **params)


class ModelFactory:
    """
    Factory class for creating machine learning models using specified features.
    By default, all features registered in [asec.features][asec.features]
    are used for training the models. You can customize by using the kwargs
    include_only (only choose a subset of registered features),
    exclude (exclude specific registered features) and add (add custom estimators to
    the feature union).
    """

    @classmethod
    def create_xgb(
        cls,
        include_only: list[FeatureName] | None = None,
        exclude: list[FeatureName] | None = None,
        add: list[Pipeline | ColumnTransformer] | None = None,
        **xgb_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        classifier = LabelEncodedClassifier(XGBClassifier(**xgb_kwargs), LabelEncoder())
        return make_pipeline(feature_union, classifier)

    @classmethod
    def create_lightgbm(
        cls,
        include_only: list[FeatureName] | None = None,
        exclude: list[FeatureName] | None = None,
        add: list[Pipeline | ColumnTransformer] | None = None,
        **lgbm_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        classifier = LabelEncodedClassifier(
            LGBMClassifier(**lgbm_kwargs), LabelEncoder()
        )
        return make_pipeline(feature_union, classifier)

    @classmethod
    def create_mlp(
        cls,
        include_only: list[FeatureName] | None = None,
        exclude: list[FeatureName] | None = None,
        add: list[Pipeline | ColumnTransformer] | None = None,
        **mlp_kwargs,
    ):
        feature_union = cls._create_feature_union(include_only, exclude, add)
        classifier = LabelEncodedClassifier(MLPClassifier(**mlp_kwargs), LabelEncoder())
        return make_pipeline(feature_union, classifier)

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


def build_pipeline(classifier: Any) -> Pipeline:
    """Constructs a preprocessing and classification pipeline.

    Parameters
    ----------
    classifier : Any
        Classifier to use in the pipeline.

    Returns
    -------
    Pipeline
        A scikit-learn pipeline with preprocessing and classifications steps.
    """

    categorical_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])
    numerical_pipeline = Pipeline([("scaler", StandardScaler())])
    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    column_transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                categorical_pipeline,
                CensusASECMetadata.CATEGORICAL_FEATURES,
            ),
            (
                "numerical_pipeline",
                numerical_pipeline,
                CensusASECMetadata.NUMERIC_FEATURES,
            ),
            (
                "ordinal_pipeline",
                ordinal_pipeline,
                CensusASECMetadata.ORDINAL_FEATURES,
            ),
        ]
    )

    return Pipeline(
        [
            ("preprocessor", column_transformer),
            ("classifier", classifier),
        ]
    )
