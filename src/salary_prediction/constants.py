from optuna.distributions import FloatDistribution, IntDistribution

from asec.data import PUMSMetaData

from .resources.configuration import (
    Config,
    NannyMLConfig,
    OptunaXGBParamDistribution,
    StratifiedShuffleCVConfig,
)

experiment_config = Config(
    random_state=495,
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
    random_state=495,
    scoring="f1",
)

optuna_xgb_param_distribution = OptunaXGBParamDistribution(
    classifier_prefix="estimator",
    max_depth=IntDistribution(3, 15),
    gamma=FloatDistribution(0.0, 5.0),
    reg_lambda=FloatDistribution(0.0, 10.0),
    learning_rate=FloatDistribution(0.01, 0.1),
    reg_alpha=FloatDistribution(0.0, 5.0),
)

nanny_ml_config = NannyMLConfig(
    chunk_size=250,
    metrics=["roc_auc"],
)
