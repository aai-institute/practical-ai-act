from dagster import Definitions

from income_prediction.assets.census_asec_features import census_asec_features
from income_prediction.assets.income_prediction_model import income_prediction_model
from income_prediction.assets.train_test import train_test_data
from income_prediction.resources.configuraton import Config
from income_prediction.resources.census_asec_downloader import CensusASECDownloader
from income_prediction.resources.mlflow_session import MlflowSession

config = Config()

definitions = Definitions(
    assets=[
        census_asec_features,
        train_test_data,
        income_prediction_model,
    ],
    resources={
        "config": config,
        "census_data_downloader": CensusASECDownloader(year=config.census_asec_dataset_year),
        "mlflow_session": MlflowSession(tracking_url=config.mlflow_tracking_url, experiment=config.mlflow_experiment),
    },
)
