from functools import partial
from typing import Sequence, Callable

from more_itertools import powerset

from sensai import VectorClassificationModel
from sensai.evaluation import (
    ClassificationEvaluatorParams,
    ClassificationModelEvaluation,
    VectorModelCrossValidatorParams,
)
from sensai.evaluation.eval_stats import ClassificationMetricAccuracy
from sensai.util import logging
from sensai.util.io import ResultWriter
from sensai.util.logging import datetime_tag
from sensai.tracking.mlflow_tracking import MLFlowExperiment


from config import FILE_NAME_ADULT, RESULT_SUBFOLDER, MLFLOW_SUBFOLDER
from adult.data import AdultData, CLASS_POSITIVE
from adult.model_factory import ModelFactory
from adult.features import FeatureName, PERSONAL_FEATURES


def create_feature_combinations(
    model_factory: Callable[[Sequence[FeatureName]], VectorClassificationModel],
    features: Sequence[FeatureName],
) -> list[VectorClassificationModel]:
    """
    Create all possible feature combinations for the given features and create a model for each combination.
    Args:
        model_factory: function to create a model based on a list of feature names
        features: list of features to create combinations from

    Returns:
        list of models with all possible feature combinations
    """
    return [model_factory(feat) for feat in powerset(features)]


def create_experiment_tag(
    ablation_feat: Sequence[FeatureName] = PERSONAL_FEATURES,
    prefix: str = "feature_ablation_study_",
) -> str:
    """
    Create a tag for the experiment based on the ablation features.
    Args:
        ablation_feat:
        prefix:

    Returns:

    """
    return prefix + "_".join([f.value for f in ablation_feat])


def main(
    models: Sequence[VectorClassificationModel],
    name: str = "feature_ablation_study",
):
    run_id = datetime_tag()
    tracked_experiment = MLFlowExperiment(
        name,
        tracking_uri=str(MLFLOW_SUBFOLDER),
        context_prefix=run_id + "_",
        add_log_to_all_contexts=True,
    )
    result_writer = ResultWriter(RESULT_SUBFOLDER / name / run_id)
    logging.add_file_logger(result_writer.path("log.txt"))

    eval_params = ClassificationEvaluatorParams(
        fractional_split_test_fraction=0.2, binary_positive_label=CLASS_POSITIVE
    )
    cross_eval_params = VectorModelCrossValidatorParams(evaluator_params=eval_params)
    adult_data = AdultData(FILE_NAME_ADULT)
    io_data = adult_data.load_input_output_data()
    evaluation = ClassificationModelEvaluation(
        io_data, evaluator_params=eval_params, cross_validator_params=cross_eval_params
    )

    evaluation.compare_models(
        models,
        fit_models=True,
        use_cross_validation=True,
        sort_column=ClassificationMetricAccuracy.name,
        sort_ascending=False,
        tracked_experiment=tracked_experiment,
        result_writer=result_writer,
    )


if __name__ == "__main__":
    ablation_features = (
        FeatureName.SEX,
        FeatureName.AGE,
        FeatureName.RACE,
        FeatureName.MARITAL_STATUS,
        FeatureName.NATIVE_COUNTRY,
        FeatureName.RELATIONSHIP,
    )
    experiment_name = create_experiment_tag(ablation_feat=ablation_features)
    xgb_models = create_feature_combinations(
        lambda x: ModelFactory.create_xgb(add_features=x), ablation_features
    )
    callable_main = partial(main, xgb_models, name=experiment_name)
    logging.run_main(callable_main, level=logging.INFO)
