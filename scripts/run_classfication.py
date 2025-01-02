
from sensai.evaluation import ClassificationEvaluatorParams, \
    ClassificationModelEvaluation

from sensai.util import logging

from config import FILE_NAME
from statlog.data import StatLogData
from statlog.model_factory import ModelFactory


def main():
    eval_params = ClassificationEvaluatorParams(fractional_split_test_fraction=0.2)
    statlog_data = StatLogData(FILE_NAME)
    io_data = statlog_data.load_input_output_data()
    evaluation = ClassificationModelEvaluation(io_data, evaluator_params=eval_params)
    models = [
        ModelFactory.create_logistic_regression(),
        ModelFactory.create_xgb(),
        ModelFactory.create_random_forest(),
        ModelFactory.create_lightgbm()
    ]

    evaluation.compare_models(models, fit_models=True)

if __name__ ==  "__main__":
    logging.run_main(main)

