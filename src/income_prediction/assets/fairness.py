import fairlearn
import fairlearn.metrics
import pandas as pd
import sklearn
import sklearn.metrics
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

from asec.data import PUMSMetaData

TARGET = PUMSMetaData.TARGET
SEX_FEATURE = PUMSMetaData.Fields.SEX

SEX_MALE = 1
SEX_FEMALE = 2

PRIVILEGED_GROUPS = [
    {SEX_FEATURE: SEX_MALE},
]
UNPRIVILEGED_GROUPS = [
    {SEX_FEATURE: SEX_FEMALE},
]


def _make_dataset(data: pd.DataFrame) -> StandardDataset:
    df = data.copy()
    return StandardDataset(
        df,
        label_name=PUMSMetaData.TARGET,
        favorable_classes=[1],
        protected_attribute_names=[
            SEX_FEATURE,
        ],
        privileged_classes=[
            [SEX_MALE],
        ],
    )


def extract_metrics(dm: BinaryLabelDatasetMetric) -> dict:
    """Extracts fairness metrics of interest from a BinaryLabelDatasetMetric instance."""
    metric_fns = [
        BinaryLabelDatasetMetric.disparate_impact,
        BinaryLabelDatasetMetric.statistical_parity_difference,
        BinaryLabelDatasetMetric.mean_difference,
    ]
    metrics = {}
    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn(dm)
        metrics[metric_name] = metric_value

    return metrics


def dataset_metrics(data: pd.DataFrame) -> BinaryLabelDatasetMetric:
    ground_truth = _make_dataset(data)
    return BinaryLabelDatasetMetric(
        ground_truth,
        unprivileged_groups=UNPRIVILEGED_GROUPS,
        privileged_groups=PRIVILEGED_GROUPS,
    )


def classification_metrics(
    data: pd.DataFrame, predictions: pd.Series
) -> ClassificationMetric:
    ground_truth = _make_dataset(data)

    predictions_data = ground_truth.copy(deepcopy=True)
    predictions_data.labels = predictions

    return ClassificationMetric(
        ground_truth,
        predictions_data,
        unprivileged_groups=UNPRIVILEGED_GROUPS,
        privileged_groups=PRIVILEGED_GROUPS,
    )


def make_metricframe(
    ground_truth: pd.DataFrame,
    predictions: pd.Series,
    sensitive_features: pd.Series | pd.DataFrame,
) -> fairlearn.metrics.MetricFrame:
    return fairlearn.metrics.MetricFrame(
        metrics={
            "accuracy": sklearn.metrics.accuracy_score,
            "selection_rate": fairlearn.metrics.selection_rate,
            "count": fairlearn.metrics.count,
        },
        y_true=ground_truth[[TARGET]],
        y_pred=predictions,
        sensitive_features=sensitive_features,
    )
