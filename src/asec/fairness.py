from typing import Any

import dagster as dg
import pandas as pd
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

from asec.data import PUMSMetaData

NEGATIVE_OUTCOME = 0
POSITIVE_OUTCOME = 1


class ProtectedAttributes(dg.Config):
    privileged_groups: list[dict[str, Any]]
    unprivileged_groups: list[dict[str, Any]]

    @property
    def protected_attribute_names(self) -> list[str]:
        attrs = set()
        for grp in self.privileged_groups:
            attrs = attrs.union(set(grp.keys()))
        return list(attrs)

    @property
    def privileged_protected_attributes(self) -> Any | list[Any]:
        def _privileged_val(attr):
            grp = [g[attr] for g in self.privileged_groups if attr in g.keys()]
            if len(grp) != 1:
                raise ValueError("fubar")
            return grp[0]

        if len(self.protected_attribute_names) == 1:
            return _privileged_val(self.protected_attribute_names[0])
        else:
            raise NotImplementedError()

    @property
    def unprivileged_protected_attributes(self) -> list[list[Any]]:
        def _unprivileged_val(attr):
            return [g[attr] for g in self.unprivileged_groups if attr in g.keys()]

        return [_unprivileged_val(attr) for attr in self.protected_attribute_names]


class AcsPumsDataset(BinaryLabelDataset):
    def __init__(self, df: pd.DataFrame, protected_attributes: ProtectedAttributes):
        super().__init__(
            df=df,
            favorable_label=POSITIVE_OUTCOME,
            unfavorable_label=NEGATIVE_OUTCOME,
            label_names=[PUMSMetaData.TARGET],
            protected_attribute_names=protected_attributes.protected_attribute_names,
            unprivileged_protected_attributes=protected_attributes.unprivileged_protected_attributes,
            privileged_protected_attributes=protected_attributes.privileged_protected_attributes,
        )


def extract_metrics(
    *,
    protected_attributes: ProtectedAttributes,
    y_true: pd.Series,
    y_pred: pd.Series | None = None,
) -> dict[str, float]:
    """Extracts fairness metrics of interest from a BinaryLabelDatasetMetric instance."""

    from aif360.sklearn.metrics import (
        disparate_impact_ratio,
        mean_difference,
        statistical_parity_difference,
    )

    metric_fns = [
        disparate_impact_ratio,
        statistical_parity_difference,
        mean_difference,
    ]
    metrics = {}
    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn.__call__(
            y_true=y_true,
            y_pred=y_pred,
            pos_label=POSITIVE_OUTCOME,
            prot_attr=protected_attributes.protected_attribute_names[0]
            if len(protected_attributes.protected_attribute_names) == 1
            else protected_attributes.protected_attribute_names,
            priv_group=protected_attributes.privileged_protected_attributes,
        )

        # Convert numpy floats to native Python floats to avoid serialization issues in Dagster
        metrics[metric_name] = float(metric_value)

    return metrics


def dataset_metrics(
    data: pd.DataFrame, protected_attributes: ProtectedAttributes
) -> BinaryLabelDatasetMetric:
    ground_truth = AcsPumsDataset(data.copy(), protected_attributes)
    return BinaryLabelDatasetMetric(
        ground_truth,
        unprivileged_groups=protected_attributes.unprivileged_groups,
        privileged_groups=protected_attributes.privileged_groups,
    )


def classification_metrics(
    data: pd.DataFrame,
    predictions: pd.Series,
    protected_attributes: ProtectedAttributes,
) -> ClassificationMetric:
    ground_truth = AcsPumsDataset(data.copy(), protected_attributes)

    predictions_data = ground_truth.copy(deepcopy=True)
    predictions_data.labels = predictions

    return ClassificationMetric(
        ground_truth,
        predictions_data,
        unprivileged_groups=protected_attributes.unprivileged_groups,
        privileged_groups=protected_attributes.privileged_groups,
    )


pa = ProtectedAttributes(
    privileged_groups=[{PUMSMetaData.Fields.SEX: PUMSMetaData.SEX_MALE}],
    unprivileged_groups=[{PUMSMetaData.Fields.SEX: PUMSMetaData.SEX_FEMALE}],
)
print(pa.protected_attribute_names)
print("Unpriv attr", pa.unprivileged_protected_attributes)
print("Priv attr", pa.privileged_protected_attributes)
print("Unpriv group", pa.unprivileged_groups)

#
# df = pd.read_parquet("lakefs://twai-pipeline/main/data/train_data.parquet")
# ds = AcsPumsDataset(df, pa)
#
# dm = dataset_metrics(df, pa)
# print(dm.disparate_impact())
