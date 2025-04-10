---
tags:
    - Art. 10
    - Art. 11
---

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 10(2)(c)|**: Consistent and versioned data preprocessing operations
    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation), in particular:
        - |Annex IV(2)(c)|: Description of the system and overall processing architecture

## Motivation

The orchestration of machine learning workflows is a critical aspect of the machine learning lifecycle.

In essence, it concerns the automated execution of tasks such as data preprocessing, model training, evaluation, and deployment.

A workflow orchestrator takes care to execute these tasks in the correct order, manage dependencies between tasks, and handle failures or retries as needed.
It keeps a permanent record of the execution history, which is essential for reproducibility, transparency, and auditability.

## Implementation Notes

TODO

## Key Technologies

### Workflow Orchestrators

-   [Dagster](https://dagster.io/)
-   [Apache Airflow](https://airflow.apache.org/)
-   [Prefect](https://prefect.io/)
-   [Flyte](https://flyte.org/)

### MLOps Platforms

-   [Kubeflow](https://kubeflow.org/)
-   [Metaflow](https://metaflow.org/)
-   [ZenML](https://zenml.io/)
-   [Kedro](https://kedro.readthedocs.io/en/stable/)

### Platform-/Software-as-a-Service Offerings

-   [AWS Step Functions](https://aws.amazon.com/step-functions/)
-   [Google Cloud Workflows](https://cloud.google.com/workflows)
-   [Databricks Workflows](https://www.databricks.com/product/workflows)
