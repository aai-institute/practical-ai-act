import warnings

import dagster as dg
import optuna
from dagster._core.storage.fs_io_manager import PickledObjectFilesystemIOManager
from upath import UPath

from salary_prediction.constants import (
    experiment_config,
    nanny_ml_config,
    optuna_cv_config,
    optuna_xgb_param_distribution,
)
from salary_prediction.io_managers.lakefs import LakeFSParquetIOManager
from salary_prediction.jobs import e2e_pipeline_job
from salary_prediction.resources.configuration import (
    LakeFsConfig,
    MinioConfig,
    MlFlowConfig,
)
from salary_prediction.resources.mlflow_session import MlflowSession
from salary_prediction.utils.dagster import get_current_env

# -- Warning control
# Dagster source code references are a beta feature, got it
warnings.filterwarnings(action="ignore", category=dg.BetaWarning)
# UPath works with lakefs-spec, warning is safe to ignore
warnings.filterwarnings(
    action="ignore", category=UserWarning, message=".*UPath 'lakefs'.*"
)
# AIF360 calls Pandas in a way that emits a warning about assigning incompatible dtypes
warnings.filterwarnings(
    action="ignore",
    category=FutureWarning,
    module="aif360.sklearn.postprocessing.calibrated_equalized_odds",
)
# OptunaSearchCV is experimental, duly acknowledged
warnings.filterwarnings(
    action="ignore",
    category=optuna.exceptions.ExperimentalWarning,
    module="optuna.integration",
)


dagster_env = get_current_env()
print("Current environment:", dagster_env)

if dagster_env == "production":
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
        secret=minio_cfg.minio_secret_access_key.get_secret_value(),
    )
else:
    default_io_manager = dg.FilesystemIOManager()
    mlflow_cfg = MlFlowConfig()
    lakefs_cfg = LakeFsConfig()
    minio_cfg = MinioConfig()

print("LakeFS config: ", lakefs_cfg)
print("MinIO config: ", minio_cfg)
print("MLflow config: ", mlflow_cfg)

definitions = dg.Definitions(
    assets=dg.with_source_code_references(
        dg.load_assets_from_package_name("salary_prediction.assets")
    ),
    asset_checks=dg.load_asset_checks_from_package_name("salary_prediction.assets"),
    jobs=[e2e_pipeline_job],
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
                username=lakefs_cfg.lakefs_access_key_id.get_secret_value(),
                password=lakefs_cfg.lakefs_secret_access_key.get_secret_value(),
                verify_ssl=lakefs_cfg.lakefs_verify_ssl,
            ),
        ),
        "optuna_cv_config": optuna_cv_config,
        "optuna_xgb_param_distribution": optuna_xgb_param_distribution,
        "nanny_ml_config": nanny_ml_config,
    },
)
