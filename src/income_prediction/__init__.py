from dagster import Definitions

from income_prediction.assets.census_asec_dataset import census_asec_dataset
from income_prediction.assets.census_asec_features import census_asec_features
from income_prediction.assets.income_prediction_model import income_prediction_model
from income_prediction.assets.train_test import train_test_data
from income_prediction.resources.configuraton import Config

definitions = Definitions(
    assets=[
        census_asec_dataset,
        census_asec_features,
        train_test_data,
        income_prediction_model,
    ],
    resources={
        "config": Config(),
    },
)
