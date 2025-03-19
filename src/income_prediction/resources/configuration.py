from typing import Any

from sklearn.model_selection import StratifiedShuffleSplit
from dagster import ConfigurableResource, ResourceDefinition
from optuna.distributions import FloatDistribution, IntDistribution
from pydantic import BaseModel


class MlFlowConfig(BaseModel):
    mlflow_tracking_url: str = "http://localhost:50000"
    mlflow_experiment: str = "Income Prediction"


class LakeFsConfig(BaseModel):
    lakefs_host: str = "http://localhost:8000"
    lakefs_access_key_id: str = "AKIAIOSFOLKFSSAMPLES"
    lakefs_secret_access_key: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    lakefs_verify_ssl: bool = False


class MinioConfig(BaseModel):
    minio_host: str = "http://localhost:9000"
    minio_access_key_id: str = "minio_user"
    minio_secret_access_key: str = "minio_password"


class Config(ConfigurableResource):
    """Pipeline configuration."""

    census_asec_dataset_year: int = 2024

    salary_bands: list[int] = [
        35000,  # Entry level
        55000,  # Lower mid-range
        85000,  # Mid-range
        120000,  # Upper mid-range
    ]  # > 120000 High

    data_dir: str = "data"

    random_state: int = 42

    log_model_explainability: bool = True


class OptunaCVConfig(ConfigurableResource):
    """
    Optuna cross-validation configuration. This resource is used to configure the
    parameters of the Optuna cross-validation search. The parameters are passed to
    the [optuna.integration.OptunaSearchCV][optuna.integration.OptunaSearchCV] class.

    This config does not specify the 'cv' parameter, so it will resolve to the default
    value from optuna
    ([sklearn.model_selection.StratifiedKFold][sklearn.model_selection.StratifiedKFold]
    with 5 splits), see the documentation of
    [optuna.integration.OptunaSearchCV][optuna.integration.OptunaSearchCV]
    for more details. If you want to use a stratified shuffle split with a custom
    validation size and number of splits, use
    [income_prediction.resources.configuration.StratifiedShuffleCVConfig][income_prediction.resources.configuration.StratifiedShuffleCVConfig]

    Args:
        n_trials: Number of trials for the optimization.
        timeout: Time limit for the optimization process in seconds.
        verbose: Verbosity level.
        n_jobs: Number of parallel jobs to run.
        random_state: Seed for the random number generator.
        refit: Whether to refit the best model on the whole dataset.
        scoring: Scoring strategy to evaluate the performance of the cross-validated
            model on the validation set. For more details,
            see [sklearn.metrics.get_scorer][sklearn.metrics.get_scorer]
        kwargs: Additional keyword arguments to pass to the OptunaSearchCV class.
    """

    n_trials: int = 100
    timeout: int = 600
    verbose: int = 2
    n_jobs: int = -1
    random_state: int
    refit: bool = True
    scoring: str = "accuracy"
    kwargs: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "n_trials": self.n_trials,
            "timeout": self.timeout,
            "verbose": self.verbose,
            "n_jobs": self.n_jobs,
            "random_state": self.random_state,
            "refit": self.refit,
            "scoring": self.scoring,
            **(self.kwargs or {}),
        }


class StratifiedShuffleCVConfig(OptunaCVConfig):
    """
    Optuna cross-validation configuration. This resource is used to configure the
    parameters of the Optuna cross-validation search. The parameters are passed to
    the [optuna.integration.OptunaSearchCV][optuna.integration.OptunaSearchCV] class.
    It causes optuna to use a stratified shuffle split cross-validator with
    user defined validation size and number of splits.

    Args:
        n_trials: Number of trials for the optimization.
        timeout: Time limit for the optimization process in seconds.
        verbose: Verbosity level.
        n_jobs: Number of parallel jobs to run.
        random_state: Seed for the random number generator.
        refit: Whether to refit the best model on the whole dataset.
        scoring: Scoring strategy to evaluate the performance of the cross-validated
            model on the validation set. For more details,
            see [sklearn.metrics.get_scorer][sklearn.metrics.get_scorer]
        validation_size: Fraction of the dataset to include in the validation split.
        kwargs: Additional keyword arguments to pass to the OptunaSearchCV class.

    """

    validation_size: float = 0.2
    n_splits: int = 5

    def as_dict(self) -> dict[str, Any]:
        config_dict = super().as_dict()
        config_dict["cv"] = StratifiedShuffleSplit(
            self.n_splits,
            test_size=self.validation_size,
            random_state=self.random_state,
        )
        return config_dict


class OptunaXGBParamDistribution(ResourceDefinition):
    """
    Optuna distribution for XGBoost parameters. For a detailed description of the
    parameters, see the [XGBoost documentation](https://xgboost.readthedocs.io/en/stable/parameter.html#parameters-for-tree-booster).

    Args:
        max_depth: Maximum depth of a tree.
        gamma: Minimum loss reduction required to make a further partition on a leaf
            node of the tree.
        reg_lambda: L2 regularization term on weights.
        colsample_bytree: Fraction of features that will be used in each tree.
        min_child_weight: Minimum sum of instance weight (hessian) needed in a child.
        classifier_prefix: Prefix for classifier parameters. For optuna to be able to
            access and modify the parameters of a classifier within a sklearn pipeline,
            the classifier parameters must be prefixed with the name of the classifier
            step in the pipeline.
    """

    def __init__(
        self,
        max_depth: IntDistribution | None = None,
        gamma: FloatDistribution | None = None,
        reg_lambda: FloatDistribution | None = None,
        colsample_bytree: FloatDistribution | None = None,
        min_child_weight: IntDistribution | None = None,
        classifier_prefix: str | None = None,
        **kwargs: Any,
    ):
        if classifier_prefix is None:
            classifier_prefix = ""
        else:
            classifier_prefix += "__"

        distribution_dict = {
            f"{classifier_prefix}max_depth": max_depth,
            f"{classifier_prefix}gamma": gamma,
            f"{classifier_prefix}reg_lambda": reg_lambda,
            f"{classifier_prefix}colsample_bytree": colsample_bytree,
            f"{classifier_prefix}min_child_weight": min_child_weight,
            **{f"{classifier_prefix}{k}": v for k, v in kwargs.items()},
        }

        distribution_dict = {
            k: v for k, v in distribution_dict.items() if v is not None
        }

        super().__init__(resource_fn=lambda: distribution_dict)


class NannyMLConfig(ConfigurableResource):
    chunk_size: int = 200
    metrics: list[str] = ["roc_auc"]
