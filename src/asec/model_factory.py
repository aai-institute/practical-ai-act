import numpy as np
from aif360.sklearn.preprocessing import Reweighing, ReweighingMeta
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier


class ModelFactory:
    @classmethod
    def create_xgb(
        cls,
        random_state: int | np.random.RandomState,
        mitigate_bias: bool,
        sensitive_feature_names: list[str],
    ) -> BaseEstimator:
        xgb = XGBClassifier(
            enable_categorical=True,
            random_state=random_state,
        )

        if mitigate_bias:
            clf = ReweighingMeta(
                estimator=xgb,
                reweigher=Reweighing(sensitive_feature_names),
            )
        else:
            clf = Pipeline([
                (
                    "estimator",
                    xgb,
                )
            ])

        return clf
