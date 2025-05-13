---
tags:
    - Art. 12
    - Art. 14
    - Art. 15
    - Art. 26
    - Art. 72
---

# Model Performance Monitoring

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    Implementing a model performance solution will help you in achieving compliance with the following regulations:

    - **|Art. 12|** (Record-Keeping)
        - |Art. 12(1)| (Documentation of the AI system)
    - **|Art. 14|** (Human Oversight), in particular:
        -   |Art. 14(4)(a)|, automated tracking of drift and performance degradation
            helps to understand the capacities of the system during its lifetime
        -   |Art. 14(4)(e)|, observing degradation overtime enables to intervene and
            initialize a retraining, for example
    - **|Art. 15|** (Accuracy, Robustness and Cybersecurity), in particular:
        - |Art. 15(4)|, resilience and robustness through continuous monitoring of model performance
    - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)
    - **|Art. 72(2)|** (Post-market Monitoring), since a model monitoring solution allows for the continuous monitoring of the AI system's performance and compliance with legal requirements.

## Motivation

Monitoring is important to ensure that after a deployment to production, AI systems continue to work as expected from the performance measured during the training phase.
Performance (i.e., the quality of predictions / outputs) can degrade for a number of reasons:
For example due to data drift, where the inference data is sufficiently dissimilar from the training data that predictions are off, or due to concept drift, where the probability distributions of the prediction target changes over time.
Another metric of interest is the amount (or frequency) of HTTP errors, which can be monitored to recognize unhealthy inference servers or more severe outages.

Identifying these degradations early is key to mitigate accuracy and safety concerns due to inaccuracies of deployed AI systems, especially high-risk systems presented here.

## Implementation Notes

Creating an accurate and responsive monitoring service can be challenging for multiple reasons.
Depending on the target metrics, a meaningful and easily interpretable visualization needs to be crafted, which might depend on the nature of the AI system.

As inference data and logs should be easily accessible and need to be processed efficiently for monitoring purposes (see the [inference log](inference-log.md) engineering practice), many monitoring solutions build on scalable, high-performance database systems.

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
-   Prometheus [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/), as an alerting middleware
