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

Which workflow operator to choose depends on the specific requirements for a given project, such as the complexity of the workflows, the scale of the data, and the available infrastructure.
Some orchestrators are designed for specific environments (e.g., cloud-native, on-premise), while others are more flexible and can be deployed in various settings.

When deciding on a workflow orchestrator, consider the following guiding questions:

-   Does the orchestrator support the programming language and libraries you are using?
    -   Some orchestrators are designed for specific languages or frameworks (e.g., Python, R, TensorFlow, PyTorch), while others allow you to mix and match different languages and libraries, even within a single workflow.
    -   Some orchestrators can delegate specific task types to other platforms (e.g., running an ETL job on Snowflake).
-   Does it enable seamless transition between development and production environments?
    -   Does it support local development and testing of workflows?
    -   Can workflows execute both in a cloud environment and on-premise?
-   How does it handle task dependencies and execution order?
-   How does it handle resource management?
    -   Most importantly for machine learning workloads, how does it manage GPU resources?
-   How can you access the execution history and logs for debugging and auditing purposes?
-   Does it provide built-in support for monitoring and alerting on workflow execution?
-   If required by your organization, does it support role-based access control (RBAC) and other security features?

These questions are somewhat orthogonal to the requirements of the AI Act.
In essence, basically any orchestrator that allows for consistent execution of workflows and maintains a permanent record of the execution history can be used to comply with the requirements of the AI Act.

## Key Technologies

!!! note

    Workflow orchestration tools come in various shapes and sizes, from lightweight libraries to full-fledged platforms.

    The following list is not exhaustive, but it provides a good starting point for exploring the available options and their respective features and tradeoffs.

### Workflow Orchestrators

-   [Dagster](https://dagster.io/)
-   [Apache Airflow](https://airflow.apache.org/)
-   [Argo Workflows](https://argoproj.github.io/argo-workflows/)
-   [Prefect](https://prefect.io/)
-   [Flyte](https://flyte.org/)

### MLOps Platforms

While the above orchestrators can be used for general-purpose workflow orchestration, there are also platforms specifically designed for machine learning operations (MLOps) that provide additional features and integrations tailored to the needs of ML workflows, not limited to just orchestration:

-   [Kubeflow](https://kubeflow.org/)
-   [Metaflow](https://metaflow.org/)
-   [ZenML](https://zenml.io/)
-   [Kedro](https://kedro.readthedocs.io/en/stable/)
-   [TFX](https://www.tensorflow.org/tfx)

### Platform-/Software-as-a-Service Offerings

If you are already using a cloud provider, you may want to consider their ML pipeline orchestration products:

-   [AWS SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/)
-   [Azure Machine Learning Pipelines](https://learn.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines)
-   [Google Vertex AI Pipelines](https://cloud.google.com/ai-platform/pipelines/docs)

Or, on a lower level, you can use the workflow orchestration services provided by the cloud providers:

-   [AWS Step Functions](https://aws.amazon.com/step-functions/)
-   [Azure Data Factory](https://azure.microsoft.com/en-us/services/data-factory/)
-   [Google Cloud Workflows](https://cloud.google.com/workflows)
-   [Databricks Workflows](https://www.databricks.com/product/workflows)
