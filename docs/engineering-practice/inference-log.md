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

Rather than put inference logs as a purely static archive in a storage location, it is useful for the reasons mentioned to use a database system that allows the data to be queried efficiently and in a performant manner.

One way to achieve this is a document database (PostgreSQL, MongoDB, ...), which can be deployed as a managed service to allow the inference data to be accessed in other parts of the lifecycle, for example in a case like continuous (re-)training.
Many cloud providers offer managed PostgreSQL deployments, but there also exist Software as a Service (SaaS) companies offering such solutions to be deployed on private infrastructure as well (e.g. [Supabase](https://supabase.com/)).

In the case of a smaller-scale infrastructure of multiple machines or even a single machine, it is also possible to keep inference logs in memory for even faster access, for example using an in-memory database like [redis](https://redis.io/).

With regards to traceability of inference data, it is advisable in general to place inference logs under data version control just like the training data used in the initial training of the AI system. For a guide on how to use data version control in your project, see the [engineering practice on data versioning](data-governance/data-versioning.md).

See the [showcase](../showcase/implementation-notes/inference-logging.md) for an example how to integrate an inference log into an AI system.

## Key Technologies

-   Any database or storage solution that supports the required data structure
    -   The showcase implementation uses [PostgreSQL](https://www.postgresql.org/)
    -   Other choice include [ElasticSearch](https://www.elastic.co/elasticsearch/), [MongoDB](https://www.mongodb.com/), or [SQLite](https://www.sqlite.org/index.html)
-   [Open Inference Protocol specification](https://github.com/kserve/open-inference-protocol/), as a standardized data structure for the input and output data
-   [FastAPI](https://fastapi.tiangolo.com/) for building the AI system's application code
-   [Databricks Inference Tables](https://www.databricks.com/blog/announcing-inference-tables-simplified-monitoring-and-diagnostics-ai-models) for monitoring models after deployment
