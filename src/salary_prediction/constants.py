from optuna.distributions import FloatDistribution, IntDistribution

from asec.data import PUMSMetaData

from .resources.configuration import (
    Config,
    NannyMLConfig,
    OptunaXGBParamDistribution,
    StratifiedShuffleCVConfig,
)

RANDOM_STATE = 495

experiment_config = Config(
    random_state=RANDOM_STATE,
    model_name="salary-predictor",
    test_size=0.25,
    sample_fraction=0.3,
    pums_dataset_year=2022,
    # Salary bands
    salary_lower_bound=0,
    salary_upper_bound=45_000,
    # Fairness
    sensitive_feature_names=[PUMSMetaData.Fields.SEX],
    mitigate_bias=True,
)

optuna_cv_config = StratifiedShuffleCVConfig(
    n_trials=50,
    verbose=2,
    timeout=600,
    n_jobs=-1,
    n_splits=5,
    validation_size=0.2,
    random_state=RANDOM_STATE,
    scoring="f1",
)

optuna_xgb_param_distribution = OptunaXGBParamDistribution(
    classifier_prefix="estimator",
    min_child_weight=FloatDistribution(1e-2, 1e2, log=True),
    max_depth=IntDistribution(3, 15),
    gamma=FloatDistribution(1e-4, 1e1, log=True),
    reg_lambda=FloatDistribution(1e-4, 10.0, log=True),
    learning_rate=FloatDistribution(1e-3, 0.3, log=True),
    reg_alpha=FloatDistribution(1e-4, 10.0, log=True),
)

nanny_ml_config = NannyMLConfig(
    chunk_size=250,
    metrics=["roc_auc"],
)
