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

    mlflow_tracking_url: str = "http://localhost:50000"
    mlflow_experiment: str = "Income Prediction"

    lakefs_host: str = "http://localhost:8000"
    lakefs_access_key_id: str = "AKIAIOSFOLKFSSAMPLES"
    lakefs_secret_access_key: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    lakefs_verify_ssl: bool = False

    random_state: int = 42


class OptunaCVConfig(ConfigurableResource):
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
                def __init__(self, max_depth: IntDistribution | None = None,
                             gamma: FloatDistribution | None = None,
                             reg_lambda: FloatDistribution | None = None,
                             colsample_bytree: FloatDistribution | None = None,
                             min_child_weight: IntDistribution | None = None,
                             classifier_prefix: str | None = "classifier",
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
