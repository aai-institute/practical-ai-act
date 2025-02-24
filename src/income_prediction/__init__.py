import dagster as dg
from optuna.distributions import IntDistribution, FloatDistribution
import income_prediction.assets
from income_prediction.io_managers.csv_fs_io_manager import CSVFSIOManager
from income_prediction.resources.configuration import Config, OptunaCVConfig, \
    OptunaXGBParamDistribution
from income_prediction.resources.mlflow_session import MlflowSession

from upath import UPath


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

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([income_prediction.assets]),
    resources={
        "config": config,
        "optuna_cv_config": optuna_cv_config,
        "optuna_xgb_param_distribution": optuna_xgb_param_distribution,
        "mlflow_session": mlflow_session,
        "csv_io_manager": CSVFSIOManager(base_path=UPath("./data")),
    },
)
