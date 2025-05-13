---
tags:
    - Art. 12
---

# Inference Log

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    Implementing an inference log will help you in achieving compliance with the following regulations:

    - **|Art. 12|** (Record-Keeping), in particular:
        - **|Art. 12(1)|**, since the inference log enables the recording of events
        - **|Art. 12(2)|**, since the inference log allows the identification of potentially harmful situations and facilitates the post-market monitoring
    - **|Art. 19|** (Automatically Generated Logs)
    - **|Art. 26|** (Obligations of Deployers of High-Risk AI Systems), in particular:
        - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)
        - **|Art. 26(6)|** (Keeping of system logs by the deployer)
    - **|Art. 72|** (Post-Market Monitoring)

## Motivation

An inference log is a permanent record of all inferences made by the AI system, including the input and output data, the model used, and relevant additional metadata.

The inference log serves as the basis for monitoring the AI system's operation, ensuring that it behaves as intended and complies with legal and ethical requirements.

Logging of inference data should allow for the reconstruction of the AI system's decision-making process, including the input data, the model used, and the output data.
This is essential for understanding the AI system's behavior and for identifying and addressing any issues that may arise.

In addition to these auditability and traceability requirements, the inference log can also be used for other purposes, such as:

-   _[Model performance monitoring](model-monitoring.md)_: The inference log can be used to track the performance of the AI system over time, allowing for the identification of any degradation in performance or changes in the input data distribution.
-   _Model retraining_: The inference log can serve a source of data for retraining the AI system, allowing for continuous improvement of the model.

## Implementation Notes

When it comes to implementing an inference log, there are several key considerations to keep in mind:

-   _Data structure_: The inference log should be designed to accommodate the specific data types and structures used in the AI system. This may include JSON or JSONB fields for input and output data, as well as additional metadata. Evolution of the data schema should be considered, as the AI system and its input and outputs may change over time.
-   _Data retention_: The inference log should be designed to accommodate the data retention requirements of the AI system (e.g., the retention periods set out in |Art. 19| of the AI Act, or any other legal or regulatory requirements, such as under the GDPR).
-   _Data protection and privacy_: Access to the inference log should be restricted to authorized personnel only, and the data should be protected against unauthorized access or tampering. This may include encryption of sensitive data, as well as access controls and audit trails.
-   _Performance and scalability_: Since every inference made by the AI system will be logged, the inference log should be designed to handle the foreseeable load (both in terms of data rate and volume) and to support efficient querying and analysis. This may include the use of indexing, partitioning, or other techniques to optimize performance.

Especially for LLM applications, a variety of existing tools exist that provide tracing and logging capabilities.

See the [showcase](../showcase/implementation-notes/inference-logging.md) for an example how to implement and integrate an inference log into an AI system.

## Key Technologies

### Data Observability

-   [whylogs](https://whylogs.readthedocs.io/en/latest/), an open-source library for data logging
-   [Seldon Core](https://docs.seldon.ai/seldon-core-2), an open-source platform for deploying and managing machine learning models on Kubernetes, implements a [data flow paradigm](https://docs.seldon.ai/seldon-core-2/user-guide/data-science-monitoring/dataflow) that facilitates the logging of inference data

### Custom Implementation

-   Any database or storage solution that supports the required data structure
    -   The showcase implementation uses [PostgreSQL](https://www.postgresql.org/)
    -   Other choice include [ElasticSearch](https://www.elastic.co/elasticsearch/), [MongoDB](https://www.mongodb.com/), or [SQLite](https://www.sqlite.org/index.html)
    -   For high-performance workloads, an event-based architecture using a message broker (e.g., [Kafka](https://kafka.apache.org/) or [RabbitMQ](https://www.rabbitmq.com/)) and a stream processing framework (e.g., [Apache Flink](https://flink.apache.org/) or [Apache Spark](https://spark.apache.org/)) may be more suitable to asynchronously log the inference data
-   [Open Inference Protocol specification](https://github.com/kserve/open-inference-protocol/), as a standardized data structure for the input and output data

### LLM Tracing and Observability

!!! note

    The field of LLM tracing and observability is rapidly evolving, so this list may not be exhaustive.

-   [MLFlow Tracing](https://mlflow.org/docs/latest/tracing/), LLM tracing functionality is part of the MLflow platform
-   [Langfuse](https://www.langfuse.com/), an open-source LLM engineering platform
-   [Langtrace](https://docs.langtrace.ai/introduction), an open-source LLM observability tool based on the [OpenTelemetry](https://opentelemetry.io/) standard
-   [Langchain Tracing](https://python.langchain.com/docs/guides/tracing)
-   [Phoenix](https://docs.arize.com/phoenix), an open-source LLM observability tool, based on OpenTelemetry
-   [Tracely](https://github.com/evidentlyai/tracely) by Evidently (see above), a LLM application tracing tool based on OpenTelemetry

### Cloud ML Platforms

-   [Databricks Inference Tables](https://docs.databricks.com/aws/en/machine-learning/model-serving/inference-tables) for monitoring models after deployment (and its [Azure Databricks counterpart](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/model-serving/inference-tables))
-   [Evidently](https://evidentlyai.com/) provides tracing and dataset logging functionality as part of its paid offering
