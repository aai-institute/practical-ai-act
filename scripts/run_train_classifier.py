import logging
from typing import Protocol

import pandas as pd
from asec.evaluation import (
    ClassificationEvaluation,
    ClassificationEvaluationParams,
)
from asec.features import FeatureName
from asec.tracking import mlflow_track

from asec.model_factory import ModelFactory
from asec.data import AdultData

from config import FILE_NAME_ADULT
#
class ProbabilisticPredictor(Protocol):
    def predict(self, X, **params):
        ...
    def predict_proba(self, X, **params):
        ...


def build_reference_data(model: ProbabilisticPredictor, X: pd.DataFrame, y_true: pd.DataFrame) -> pd.DataFrame:
    reference_df = pd.DataFrame(X)
    reference_df["target"] = y_true
    reference_df["prediction"] = model.predict(X)
    reference_df["prediction_probability"] = model.predict_proba(X).tolist()

    return reference_df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_size = 0.2
    random_seed = 31
    exp_name = "income_classification"
    art_path = "models"
    model_name = "xgboost-classifier"

    # create model
    pipeline = ModelFactory.create_xgb(exclude=[FeatureName.RELATIONSHIP_ENCODED])

    # load data
    adult_data = AdultData(FILE_NAME_ADULT)
    X, y = adult_data.load_input_output_data()

    # evaluate the model
    evaluation_params = ClassificationEvaluationParams(
        test_size=test_size,
        random_seed=random_seed,
        binary_positive_class=AdultData.CLASS_POSITIVE,
    )
    evaluation = ClassificationEvaluation(X, y, evaluation_params, fit_models=True)
    evaluation_result = evaluation.evaluate(pipeline)

    X_test, y_test = evaluation.get_test_data()

    # Prepare a reference dataset for post-hoc performance evaluation
    reference_df = build_reference_data(pipeline, X_test, y_test)

    # track result
    model_uri = mlflow_track(
        pipeline, evaluation_result, exp_name, model_name, art_path, reference_data = reference_df,
    )
