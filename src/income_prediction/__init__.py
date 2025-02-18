from dagster import Definitions

from income_prediction.assets import (
    census_asec_dataset,
    income_prediction_features,
    income_prediction_model_xgboost,
    train_test_data,
    reference_dataset,
)
from income_prediction.io_managers.csv_fs_io_manager import CSVFSIOManager
from income_prediction.resources.configuration import Config
from income_prediction.resources.mlflow_session import MlflowSession

from income_prediction.resources.model_factory import XGBClassifierFactory
from asec.model_factory import build_pipeline

config = Config()
mlflow_session = MlflowSession(
    tracking_url=config.mlflow_tracking_url, experiment=config.mlflow_experiment
)
model_factory = XGBClassifierFactory(random_state=config.random_state)

definitions = Definitions(
    assets=[
        census_asec_dataset,
        income_prediction_features,
        train_test_data,
        income_prediction_model_xgboost,
        reference_dataset,
    ],
    resources={
        "config": config,
        "mlflow_session": mlflow_session,
        "csv_io_manager": CSVFSIOManager(base_dir=config.data_dir),
        "model_factory": model_factory
    },
)
