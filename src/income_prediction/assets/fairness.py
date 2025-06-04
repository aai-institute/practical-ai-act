import pandas as pd
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

from asec.data import CensusASECMetadata

TARGET = CensusASECMetadata.TARGET
SEX_FEATURE = CensusASECMetadata.Fields.GENDER

SEX_MALE = 1
SEX_FEMALE = 2

PRIVILEGED_GROUPS = [
    {SEX_FEATURE: SEX_MALE},
]
UNPRIVILEGED_GROUPS = [
    {SEX_FEATURE: SEX_FEMALE},
]

# TODO: This is a bit misleading, as the true favorable outcome is being accepted to the job, which depends on the predicted income relative to the salary bands.
HIGH_INCOME_CLASS = 4


def _make_dataset(data: pd.DataFrame) -> StandardDataset:
    return StandardDataset(
        data,
        label_name=TARGET,
        favorable_classes=[HIGH_INCOME_CLASS],
        protected_attribute_names=[
            SEX_FEATURE,
        ],
        privileged_classes=[
            [SEX_MALE],
        ],
    )


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
