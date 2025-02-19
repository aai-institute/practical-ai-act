import dagster as dg
from upath import UPath

import income_prediction.assets
from income_prediction.io_managers.lakefs import LakeFSIOManager
from income_prediction.resources.configuration import Config
from income_prediction.resources.mlflow_session import MlflowSession

config = Config()

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules(modules=[income_prediction.assets]),
    resources={
        "config": config,
        "mlflow_session": MlflowSession(
            tracking_url=config.mlflow_tracking_url,
            experiment=config.mlflow_experiment,
        ),
        "lakefs_io_manager": LakeFSIOManager(
            base_path=UPath(
                "lakefs://twai-pipeline/main/data/",
                host=config.lakefs_host,
                username=config.lakefs_access_key_id,
                password=config.lakefs_secret_access_key,
                verify_ssl=config.lakefs_verify_ssl,
            ),
        ),
    },
)
