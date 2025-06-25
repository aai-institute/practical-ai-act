from typing import Any

from dagster import ConfigurableResource, ResourceDefinition
from optuna.distributions import FloatDistribution, IntDistribution
from pydantic import BaseModel, SecretStr
from sklearn.model_selection import StratifiedShuffleSplit


class MlFlowConfig(BaseModel):
    mlflow_tracking_url: str = "http://localhost:50000"
    mlflow_experiment: str = "Income Prediction"


class LakeFsConfig(BaseModel):
    lakefs_host: str = "http://localhost:8000"
    lakefs_access_key_id: SecretStr = SecretStr("AKIAIOSFOLKFSSAMPLES")
    lakefs_secret_access_key: SecretStr = SecretStr(
        "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    )
    lakefs_verify_ssl: bool = False


class MinioConfig(BaseModel):
    minio_host: str = "http://localhost:9000"
    minio_access_key_id: str = "minio_user"
    minio_secret_access_key: SecretStr = SecretStr("minio_password")


class Config(ConfigurableResource):
    """Pipeline configuration for the salary prediction model.

    This configuration class defines all parameters needed for training and evaluating
    the salary prediction model, including data processing, model training, fairness
    evaluation, and bias mitigation settings.

    Attributes:
        model_name: Name identifier for the trained model. This is used for tracking
            experiments in MLflow and identifying the model in the registry.

        sample_fraction: Fraction of the dataset to use for training (0.0 to 1.0).
            Useful for quick experiments with smaller data samples. A value of 1.0
            uses the entire dataset.

        test_size: Fraction of data to reserve for testing (0.0 to 1.0).
            The remaining data is used for training. Common values are 0.2 or 0.3.

        pums_dataset_year: Year of the PUMS (Public Use Microdata Sample) dataset
            to use. Different years may have different features or data distributions.

        salary_lower_bound: Minimum salary threshold for binary classification.

        salary_upper_bound: Maximum salary threshold for binary classification.
            Together with salary_lower_bound, defines the income classification boundaries.

        data_dir: Directory path where data files are stored. Defaults to "data".
            This is used to store the PUMS dataset files.

        random_state: Random seed for reproducibility. Used for train/test splitting,
            model initialization, and any other random operations to ensure
            consistent results across runs.

        log_model_explainability: Whether to generate and log model explainability
            artifacts (SHAP values) during training. Defaults to True.
            Disable for faster training when interpretability is not needed.

        sensitive_feature_names: List of feature names considered sensitive for
            fairness evaluation (e.g., ["sex", "race", "age"]). These features
            are analyzed for potential bias in model predictions.

        mitigate_bias: Whether to apply bias mitigation techniques during training.
            When True, the pipeline will attempt to reduce bias with respect to
            the sensitive features while maintaining model performance.
    """

    model_name: str
    sample_fraction: float

    test_size: float

    pums_dataset_year: int

    salary_lower_bound: float
    salary_upper_bound: float
    data_dir: str = "data"
    random_state: int
    log_model_explainability: bool = True

    # For fairness evaluation / bias mitigation
    sensitive_feature_names: list[str]
    mitigate_bias: bool


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
    [salary_prediction.resources.configuration.StratifiedShuffleCVConfig][salary_prediction.resources.configuration.StratifiedShuffleCVConfig]

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

    n_trials: int
    timeout: int
    verbose: int
    n_jobs: int
    random_state: int
    refit: bool = True
    scoring: str
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

    validation_size: float
    n_splits: int

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
        reg_alpha: FloatDistribution | None = None,
        colsample_bytree: FloatDistribution | None = None,
        min_child_weight: FloatDistribution | None = None,
        learning_rate: FloatDistribution | None = None,
        subsample: FloatDistribution | None = None,
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
            f"{classifier_prefix}reg_alpha": reg_alpha,
            f"{classifier_prefix}colsample_bytree": colsample_bytree,
            f"{classifier_prefix}min_child_weight": min_child_weight,
            f"{classifier_prefix}learning_rate": learning_rate,
            f"{classifier_prefix}subsample": subsample,
            **{f"{classifier_prefix}{k}": v for k, v in kwargs.items()},
        }

        distribution_dict = {
            k: v for k, v in distribution_dict.items() if v is not None
        }

        super().__init__(resource_fn=lambda: distribution_dict)


class NannyMLConfig(ConfigurableResource):
    """Configuration for NannyML Confidence-Based Performance Estimation (CBPE).

    NannyML is used to estimate model performance in production when ground truth
    is not yet available. This configuration controls how NannyML analyzes
    prediction data using CBPE.

    For more information, see:
    https://nannyml.readthedocs.io/en/stable/nannyml/nannyml.performance_estimation.confidence_based.cbpe.html

    Attributes:
        chunk_size: Number of observations per chunk for analysis. NannyML
            divides data into chunks to track performance over time. The chunk
            size should be large enough to provide reliable estimates but small
            enough to detect changes quickly.

        metrics: List of metrics to estimate using CBPE. For binary classification,
            supported metrics include:
            - "roc_auc": ROC AUC score
            - "f1": F1 score
            - "precision": Precision
            - "recall": Recall (Sensitivity)
            - "specificity": Specificity
            - "accuracy": Accuracy

            Note: CBPE estimates these metrics without requiring ground truth labels
            by using the model's predicted probabilities and calibration assumptions.
    """

    chunk_size: int
    metrics: list[str]
