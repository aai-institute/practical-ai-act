!!! danger "Work in Progress"

    The information on this page is incomplete and meant to illustrate the structure of these pages

# Model Performance Monitoring

!!! success "Compliance Info"

    --8<-- "docs/how-to/_compliance-info-box.partial"

    Implementing a model performance solution will help you in achieving compliance with the following regulations:

    - **|Art. 12|** (Record-Keeping)
        - **|Art. 12(1)|** (Documentation of the AI system)
    - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)
    - **|Art. 72(2)|** (Post-market Monitoring), since a model monitoring solution allows for the continuous monitoring of the AI system's performance and compliance with legal requirements.

## Rationale

TODO: Explain why model performance monitoring is important.

## Implementation Notes

### Model Performance

Estimating the performance of a model is a crucial part of the machine learning lifecycle.

For supervised learning application, the availability of labeled data poses a significant challenge.
Algorithms that can estimate a model's performance in the absence of ground truth data can help in these scenarios.

The NannyML library implements two approaches to model performance estimation:

-   _Confidence-based performance estimation_ (CBPE) for classification tasks
-   _Direct Loss Estimation_ (DLE) for regression tasks

### Data Quality

Changes in the distribution of input or ground thrust data can lead to a decrease in model performance.
**Data drift detection** aims to identify these changes after model deployment and is crucial to maintaining the model's performance.

### Reporting

NannyML performance estimators operate on _chunks_ of model predictions, which can be used to generate reports on the model's performance.

It is therefore straightforward to generate periodic reports on the model's performance.
These reports can be used to monitor the model's performance over time and identify potential issues (see the next section).

### Alerting

When a model's performance drops below a certain threshold or data drift occurs, it is essential to alert the responsible team.
NannyML allows threshold-based alerting for both performance and drift metrics, which can serve as the decision basis for the alerting system.

The concrete implementation of the alerting system depends on the organization's requirements and the available infrastructure.
Examples include sending an email or Slack message, creating a ticket in a ticketing system, or invoking a webhook.

## Key Technologies

-   [NannyML](https://www.nannyml.com/library), used in the showcase implementation
-   Alternatives for model and data quality monitoring:
    -   [Evidently](https://www.evidentlyai.com/evidently-oss), for model performance and data quality monitoring
    -   [Alibi Detect](https://docs.seldon.io/projects/alibi-detect/en/stable/), for outlier and drift detection
    -   [Pandera](https://pandera.readthedocs.io/en/stable/), for data quality validation
    -   [Great Expectations / GX Core](https://docs.greatexpectations.io/docs/core/introduction/), for data quality validation
-   Prometheus [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/), as an alerting middleware
