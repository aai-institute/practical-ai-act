from typing import Any

import dagster as dg
import pandas as pd

NEGATIVE_OUTCOME = 0
POSITIVE_OUTCOME = 1


class ProtectedAttributes(dg.Config):
    """Configuration for protected attributes and privileged classes.

    Protected attributes are defined as a dictionary where keys are attribute names
    and values are the privileged classes for those attributes.

    This class can be to pass protected attributes and privileged groups to metrics
    functions in the AIF360 sklearn metrics API."""

    privileged_classes: dict[str, Any]

    @property
    def attribute_names(self) -> str | list[str]:
        keys = list(self.privileged_classes.keys())
        if len(keys) == 1:
            return keys[0]
        else:
            return keys

    @property
    def privileged_groups(self) -> str | tuple:
        values = list(self.privileged_classes.values())
        if len(values) == 1:
            return values[0]
        else:
            return tuple(values)


def fairness_metrics(
    *,
    prot_attr: ProtectedAttributes,
    y_true: pd.Series,
    y_pred: pd.Series | None = None,
) -> dict[str, float]:
    """Calculate fairness metrics of interest from true or predicted labels.

    Note that the label series must contain the protected attributes as part of their index.
    """

    from aif360.sklearn.metrics import (
        average_odds_difference,
        disparate_impact_ratio,
        equal_opportunity_difference,
        statistical_parity_difference,
    )

    # Generally applicable metrics (i.e., do not require predictions)
    metric_fns = [
        disparate_impact_ratio,
        statistical_parity_difference,
    ]

    # Some fairness metrics require predictions
    if y_pred is not None:
        metric_fns += [
            equal_opportunity_difference,
            average_odds_difference,
        ]

    metrics = {}
    for metric_fn in metric_fns:
        metric_name = metric_fn.__name__
        metric_value = metric_fn.__call__(
            y_true=y_true,
            y_pred=y_pred,
            pos_label=POSITIVE_OUTCOME,
            prot_attr=prot_attr.attribute_names,
            priv_group=prot_attr.privileged_groups,
        )

        # Convert numpy floats to native Python floats to avoid serialization issues in Dagster
        metrics[metric_name] = float(metric_value)

    return metrics
