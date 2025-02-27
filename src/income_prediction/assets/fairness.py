import pandas as pd
from aif360.datasets import StandardDataset
from aif360.metrics import ClassificationMetric

from asec.data import CensusASECMetadata

TARGET = CensusASECMetadata.TARGET

MARITAL_STATUS_FEATURE = CensusASECMetadata.Fields.MARITAL_STATUS

IS_MARRIED = 1
IS_NOT_MARRIED = 0

PRIVILEGED_GROUPS = [{MARITAL_STATUS_FEATURE: IS_MARRIED}]
UNPRIVILEGED_GROUPS = [{MARITAL_STATUS_FEATURE: IS_NOT_MARRIED}]

HIGH_INCOME_CLASS = 1


def evaluate_fairness(
    data: pd.DataFrame, predictions: pd.Series
) -> ClassificationMetric:
    ground_truth = StandardDataset(
        data,
        label_name=TARGET,
        favorable_classes=[HIGH_INCOME_CLASS],
        protected_attribute_names=[MARITAL_STATUS_FEATURE],
        privileged_classes=[[IS_MARRIED]],
    )

    predictions_data = ground_truth.copy(deepcopy=True)
    predictions_data.labels = predictions

    metrics = ClassificationMetric(
        ground_truth,
        predictions_data,
        unprivileged_groups=UNPRIVILEGED_GROUPS,
        privileged_groups=PRIVILEGED_GROUPS,
    )
    return metrics
