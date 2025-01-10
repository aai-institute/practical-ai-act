from functools import partial

from numpy.random.mtrand import Sequence

from more_itertools import powerset
from sensai.evaluation import (
    ClassificationEvaluatorParams,
    ClassificationModelEvaluation,
)
from sensai.evaluation.eval_stats import ClassificationMetricAccuracy
from sensai.util import logging
from sensai.util.io import ResultWriter
from sensai.util.logging import datetime_tag
from sensai.tracking.mlflow_tracking import MLFlowExperiment


from config import FILE_NAME_ADULT, RESULT_SUBFOLDER
from adult.data import AdultData, CLASS_POSITIVE
from adult.model_factory import ModelFactory
from adult.features import FeatureName

PERSONAL_FEATURES = (
    FeatureName.SEX,
    FeatureName.AGE,
    FeatureName.RACE,
    FeatureName.MARITAL_STATUS,
    FeatureName.NATIVE_COUNTRY,
    FeatureName.RELATIONSHIP,
)

def main(
    ablation_features: Sequence[FeatureName] = PERSONAL_FEATURES,
):
    experiment_name = f"feature_ablation_study_" + "_".join([f.value for f in ablation_features])
    run_id = datetime_tag()
    tracked_experiment = MLFlowExperiment(
        experiment_name,
        tracking_uri="",
        context_prefix=run_id + "_",
        add_log_to_all_contexts=True,
    )
    result_writer = ResultWriter(RESULT_SUBFOLDER / experiment_name / run_id)
    logging.add_file_logger(result_writer.path("log.txt"))

    eval_params = ClassificationEvaluatorParams(
        fractional_split_test_fraction=0.2, binary_positive_label=CLASS_POSITIVE
    )
    adult_data = AdultData(FILE_NAME_ADULT)
    io_data = adult_data.load_input_output_data()
    evaluation = ClassificationModelEvaluation(io_data, evaluator_params=eval_params)


    models = [
        ModelFactory.create_xgb(add_features=feat)
        for feat in powerset(ablation_features)
    ]

    evaluation.compare_models(
        models,
        fit_models=True,
        sort_column=ClassificationMetricAccuracy.name,
        sort_ascending=False,
        tracked_experiment=tracked_experiment,
        result_writer=result_writer,
    )


if __name__ == "__main__":
    ablation_feat = (
        FeatureName.SEX,
        FeatureName.AGE,
        FeatureName.RACE,
        FeatureName.MARITAL_STATUS,
        FeatureName.NATIVE_COUNTRY,
        FeatureName.RELATIONSHIP,
    )
    callable_main = partial(main, ablation_features=ablation_feat)
    logging.run_main(main)
