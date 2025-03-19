import os
from typing import Literal

import dagster as dg
from dagster._core.storage.fs_io_manager import PickledObjectFilesystemIOManager
from optuna.distributions import FloatDistribution, IntDistribution
from upath import UPath

import income_prediction.assets
from income_prediction.io_managers.lakefs import LakeFSParquetIOManager
from income_prediction.resources.configuration import (
    Config,
    LakeFsConfig,
    MinioConfig,
    MlFlowConfig,
    NannyMLConfig,
    OptunaXGBParamDistribution,
    StratifiedShuffleCVConfig,
)
from income_prediction.resources.mlflow_session import MlflowSession

from .assets.model import ModelVersion
from .sensors import model_version_trigger

RANDOM_STATE = 495
experiment_config = Config(random_state=RANDOM_STATE)
optuna_cv_config = StratifiedShuffleCVConfig(
    n_trials=10,
    verbose=2,
    timeout=600,
    n_jobs=-1,
    n_splits=5,
    validation_size=0.2,
    random_state=experiment_config.random_state,
    scoring="f1_macro",
)
optuna_xgb_param_distribution = OptunaXGBParamDistribution(
    max_depth=IntDistribution(3, 10),
    gamma=FloatDistribution(0, 9),
    reg_lambda=FloatDistribution(0, 1),
    colsample_bytree=FloatDistribution(0.25, 1),
    min_child_weight=IntDistribution(1, 100),
    classifier_prefix="classifier",
)


def get_current_env() -> Literal["development", "production"]:
    """Determine the current Dagster environment."""
    in_dagster_dev = os.environ.get("DAGSTER_IS_DEV_CLI") == "1"
    env = "development" if in_dagster_dev else "production"
    return env


env = get_current_env()
print("Current environment:", env)

if env == "production":
    lakefs_cfg = LakeFsConfig(
        lakefs_host="http://lakefs:8000",
    )
    mlflow_cfg = MlFlowConfig(
        mlflow_tracking_url="http://mlflow:5000",
    )
    minio_cfg = MinioConfig(minio_host="http://minio:9000")
    default_io_manager = PickledObjectFilesystemIOManager(
        "s3://dagster/",
        endpoint_url=minio_cfg.minio_host,
        key=minio_cfg.minio_access_key_id,
        secret=minio_cfg.minio_secret_access_key,
    )
else:
    default_io_manager = dg.FilesystemIOManager()
    mlflow_cfg = MlFlowConfig()
    lakefs_cfg = LakeFsConfig()
    minio_cfg = MinioConfig()

print("LakeFS config: ", lakefs_cfg)
print("MinIO config: ", minio_cfg)
print("MLflow config: ", mlflow_cfg)

nanny_ml_config = NannyMLConfig(chunk_size=250)
definitions = dg.Definitions(
    assets=dg.with_source_code_references(
        dg.load_assets_from_modules(modules=[income_prediction.assets])
    ),
    sensors=[model_version_trigger],
    resources={
        "experiment_config": experiment_config,
        "mlflow_session": MlflowSession(
            tracking_url=mlflow_cfg.mlflow_tracking_url,
            experiment=mlflow_cfg.mlflow_experiment,
        ),
        "io_manager": default_io_manager,
        "lakefs_io_manager": LakeFSParquetIOManager(
            base_path=UPath(
                "lakefs://twai-pipeline/main/data/",
                host=lakefs_cfg.lakefs_host,
                username=lakefs_cfg.lakefs_access_key_id,
                password=lakefs_cfg.lakefs_secret_access_key,
                verify_ssl=lakefs_cfg.lakefs_verify_ssl,
            ),
        ),
        "optuna_cv_config": optuna_cv_config,
        "optuna_xgb_param_distribution": optuna_xgb_param_distribution,
        "model_version": ModelVersion.configure_at_launch(),
        "nanny_ml_config": nanny_ml_config,
    },
)
