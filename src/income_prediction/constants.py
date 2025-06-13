from optuna.distributions import FloatDistribution, IntDistribution

from .resources.configuration import (
    Config,
    NannyMLConfig,
    OptunaXGBParamDistribution,
    StratifiedShuffleCVConfig,
)

RANDOM_STATE = 495
experiment_config = Config(
    random_state=RANDOM_STATE,
    test_size=0.25,
    salary_upper_bound=45_000,
    sample_fraction=0.2,
)
optuna_cv_config = StratifiedShuffleCVConfig(
    n_trials=50,
    verbose=2,
    timeout=600,
    n_jobs=-1,
    n_splits=5,
    validation_size=0.2,
    random_state=experiment_config.random_state,
    scoring="f1",
)
optuna_xgb_param_distribution = OptunaXGBParamDistribution(
    max_depth=IntDistribution(3, 15),
    gamma=FloatDistribution(0.0, 5.0),
    reg_lambda=FloatDistribution(0.0, 10.0),
    colsample_bytree=FloatDistribution(0.25, 1),
    min_child_weight=IntDistribution(2, 20),
    learning_rate=FloatDistribution(0.01, 0.1),
    subsample=FloatDistribution(0.5, 0.9),
    reg_alpha=FloatDistribution(0.0, 5.0),
)

nanny_ml_config = NannyMLConfig(chunk_size=250)
