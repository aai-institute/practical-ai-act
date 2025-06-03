from optuna.distributions import FloatDistribution, IntDistribution

from .resources.configuration import (
    Config,
    NannyMLConfig,
    OptunaXGBParamDistribution,
    StratifiedShuffleCVConfig,
)

RANDOM_STATE = 495
experiment_config = Config(random_state=RANDOM_STATE, test_size=0.25)
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

nanny_ml_config = NannyMLConfig(chunk_size=250)
