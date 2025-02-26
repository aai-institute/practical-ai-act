import os

import dagster as dg
from dagster._core.storage.fs_io_manager import PickledObjectFilesystemIOManager
from upath import UPath

import income_prediction.assets
from income_prediction.io_managers.lakefs import LakeFSIOManager
from income_prediction.resources.configuration import Config
import dagster as dg
from optuna.distributions import IntDistribution, FloatDistribution
import income_prediction.assets
from income_prediction.io_managers.csv_fs_io_manager import CSVFSIOManager
from income_prediction.resources.configuration import Config, OptunaCVConfig, \
    OptunaXGBParamDistribution
from income_prediction.resources.mlflow_session import MlflowSession

config = Config()
optuna_cv_config = OptunaCVConfig(
    n_trials=10,
    verbose=2,
    timeout=600,
    n_jobs=-1
)
optuna_xgb_param_distribution = OptunaXGBParamDistribution(
    max_depth=IntDistribution(3, 10),
    gamma=FloatDistribution(0, 9),
    reg_lambda=FloatDistribution(0, 1),
    colsample_bytree=FloatDistribution(0.25, 1),
    min_child_weight=IntDistribution(1, 100),
    classifier_prefix="classifier",
)
mlflow_session = MlflowSession(
    tracking_url=config.mlflow_tracking_url, experiment=config.mlflow_experiment
)

if os.environ.get("environment", None) == "docker":
    default_io_manager = PickledObjectFilesystemIOManager(
        "s3://dagster/",
        endpoint_url=config.minio_host,
        key=config.minio_access_key_id,
        secret=config.minio_secret_access_key,
    )
else:
    default_io_manager = dg.FilesystemIOManager()

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules(modules=[income_prediction.assets]),
    resources={
        "config": config,
        "mlflow_session": MlflowSession(
            tracking_url=config.mlflow_tracking_url,
            experiment=config.mlflow_experiment,
        ),
        "io_manager": default_io_manager,
        "lakefs_io_manager": LakeFSIOManager(
            base_path=UPath(
                "lakefs://twai-pipeline/main/data/",
                host=config.lakefs_host,
                username=config.lakefs_access_key_id,
                password=config.lakefs_secret_access_key,
                verify_ssl=config.lakefs_verify_ssl,
            ),
        ),
        "optuna_cv_config": optuna_cv_config,
        "optuna_xgb_param_distribution": optuna_xgb_param_distribution,
    },
)
