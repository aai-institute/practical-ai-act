
from sensai.evaluation import ClassificationEvaluatorParams, \
    ClassificationModelEvaluation

from sensai.util import logging

from config import FILE_NAME_ADULT
from adult.data import AdultData, CLASS_POSITIVE
from adult.model_factory import ModelFactory


def main():
    eval_params = ClassificationEvaluatorParams(fractional_split_test_fraction=0.2, binary_positive_label=CLASS_POSITIVE)
    adult_data = AdultData(FILE_NAME_ADULT, dropna=False)
    io_data = adult_data.load_input_output_data()
    evaluation = ClassificationModelEvaluation(io_data, evaluator_params=eval_params)
    models = [
        ModelFactory.create_logistic_regression(),
        ModelFactory.create_xgb(),
        #ModelFactory.create_random_forest(),
        ModelFactory.create_lightgbm()
    ]

    evaluation.compare_models(models, fit_models=True)

if __name__ ==  "__main__":
    logging.run_main(main)

