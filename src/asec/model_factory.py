from typing import Any

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    LabelEncoder,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)
from sklearn.utils.metaestimators import available_if
from xgboost import XGBClassifier

from .data import PUMSMetaData


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

    def set_params(self, **params):
        self.classifier.set_params(**params)

    @available_if(lambda self: hasattr(self.classifier, "score"))
    def score(self, X, y, **params):
        return self.classifier.score(X, self.encoder.transform(y), **params)

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

    exclude = (PUMSMetaData.Fields.ANNUAL_INCOME, )

    @classmethod
    def create_xgb(
        cls,
        **xgb_kwargs,
    ):
        classifier = XGBClassifier(enable_categorical=True, **xgb_kwargs)
        return build_pipeline(
            classifier, exclude=cls.exclude, encode_categoricals=False
        )

    @classmethod
    def create_lightgbm(
        cls,
        **lgbm_kwargs,
    ):
        from lightgbm import LGBMClassifier

        classifier = LabelEncodedClassifier(
            LGBMClassifier(**lgbm_kwargs), LabelEncoder()
        )
        return build_pipeline(classifier, exclude=cls.exclude)

    @classmethod
    def create_mlp(
        cls,
        **mlp_kwargs,
    ):
        classifier = LabelEncodedClassifier(MLPClassifier(**mlp_kwargs), LabelEncoder())
        return build_pipeline(classifier, exclude=cls.exclude)


def build_pipeline(classifier: Any, exclude=None, include_only=None, encode_categoricals=True) -> Pipeline:
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

    categorical_pipeline = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    numerical_pipeline = Pipeline([("scaler", StandardScaler())])
    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    def filter_features(feat_list: list[str]):
      if include_only is not None:
        feat_list = [f for f in feat_list if f in include_only]
      if exclude is not None:
        feat_list = [f for f in feat_list if f not in exclude]
      return feat_list

    categorical_features = filter_features(PUMSMetaData.CATEGORICAL_FEATURES)
    numerical_features = filter_features(PUMSMetaData.NUMERIC_FEATURES)
    ordinal_features = filter_features(PUMSMetaData.ORDINAL_FEATURES)

    column_transformer = ColumnTransformer([
        (
            "categorical_pipeline",
            categorical_pipeline if encode_categoricals else "passthrough",
            categorical_features
        ),
        (
            "numerical_pipeline",
            numerical_pipeline,
            numerical_features
        ),
        (
            "ordinal_pipeline",
            ordinal_pipeline,
            ordinal_features,
        ),
    ])

    return Pipeline([
        ("preprocessor", column_transformer),
        ("classifier", classifier),
    ])
