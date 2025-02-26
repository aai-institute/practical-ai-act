from typing import Any
from optuna.distributions import IntDistribution, FloatDistribution
from dagster import ConfigurableResource, ResourceDefinition


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

    # FIXME: This is dependent on the environment and should be set outside the resource

    mlflow_tracking_url: str = "http://localhost:50000"
    mlflow_experiment: str = "Income Prediction"

    lakefs_host: str = "http://localhost:8000"
    lakefs_access_key_id: str = "AKIAIOSFOLKFSSAMPLES"
    lakefs_secret_access_key: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    lakefs_verify_ssl: bool = False

    minio_host: str = "http://localhost:9000"
    minio_access_key_id: str = "minio_user"
    minio_secret_access_key: str = "minio_password"

    random_state: int = 42


class OptunaCVConfig(ConfigurableResource):
    """
    Optuna cross-validation configuration. This resource is used to configure the
    parameters of the Optuna cross-validation search. The parameters are passed to
    the [optuna.integration.OptunaSearchCV][optuna.integration.OptunaSearchCV] class.
    """
    n_trials: int = 100
    timeout: int = 600
    verbose: int = 2
    n_jobs: int = -1
    random_state: int = 495
    refit: bool = True
    kwargs: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "n_trials": self.n_trials,
            "timeout": self.timeout,
            "verbose": self.verbose,
            "n_jobs": self.n_jobs,
            "random_state": self.random_state,
            "refit": self.refit,
            **(self.kwargs or {})
        }

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
    def __init__(self, max_depth: IntDistribution | None = None,
                 gamma: FloatDistribution | None = None,
                 reg_lambda: FloatDistribution | None = None,
                 colsample_bytree: FloatDistribution | None = None,
                 min_child_weight: IntDistribution | None = None,
                 classifier_prefix: str | None = None,
                 **kwargs: Any):

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
            **{f"{classifier_prefix}{k}": v for k, v in kwargs.items()}
        }

        distribution_dict = {k: v for k, v in distribution_dict.items() if v is not None}

        super().__init__(resource_fn=lambda: distribution_dict)
