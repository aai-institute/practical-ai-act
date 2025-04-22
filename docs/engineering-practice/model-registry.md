---
tags:
    - Art. 11
    - Art. 72
    - Annex IV
---

# Model registry

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation), in particular:
        - |Annex IV(2)(a)|: Description of the methods used for development of the system
        - |Annex IV(2)(c)|: Description of the system and overall processing architecture
        - |Annex IV(3)|: Description of the data and model lifecycle management
        - |Annex IV(6)|: References to model versions can help in describing relevant changes to the system through its lifecycle
    - **|Art. 13|, in particular:
        - |Art. 13(3)(b)(iv)|: Logging the model architecture and hyperparameters makes the system characteristics transparent
    - **|Art. 72|** (Post-Market Monitoring by Providers): a model registry can be used to correlate post-market monitoring data with specific model versions

## Motivation

After training and evaluation, the resulting machine learning models need to be stored for later use (e.g. for deployment in production environments).
Frequently, multiple versions of a given model are trained in parallel to assess the influence of certain parameters on the quality of the model outputs.

This, together with the requirement for reproducibility in many AI projects, necessitates a solution for managing multiple versions of models side-by-side, that is also highly available, reliable, and can be queried efficiently for any specific version.

Model registries are designed to fulfill this need by providing a repository for storing and managing machine learning models, their metadata, and lineage.
Advanced functionality can include the ability to manage the lifecycle of models, including versioning, deployment, and monitoring.

The model registry fills a crucial role as the bridge between the development and operational phases of the machine learning lifecycle.
They API is typically provided to allow for easy integration with other tools and processes, such as continuous deployment pipelines, validation activities, and triggering of workflows in an orchestration system.

## Implementation notes

Capabilities of a model registry can vary quite widely depending on how much of the stated responsibilities are handled by other tools in the practitioner's AI tool stack of choice.

In the simplest case, a model registry can just be a local or remote storage bucket, that keeps track of model metadata and versions by indexing them and storing the information in a database or similar systems.
If more responsibilities for the AI model lifecycle need to be handled, it is possible to use a tool that combines the storage of artifacts with their deployment, e.g. as a web application or a local assistant type of model.

In any case, the model registry should be able to store the model artifacts in a versioned manner, so that it is possible to retrieve any version of a model at any time.

## Key Technologies

Since the task of versioning and storing models is tightly coupled to the tracking of metadata and metrics about the model training process, many [experiment tracking](experiment-tracking.md)) solutions come with a builtin model registry that allows for models resulting from an experiment run to be tracked.

Additionally, model registry functionality is commonly included in MLOps platforms, which are designed to cover the entire machine learning lifecycle (see the page on [workflow orchestration](orchestration.md)).

Besides bespoke model registry solutions, models can also be stored in a suitable [versioned data storage](data-governance/data-versioning.md) system or container registry (for [containerized](containerization.md) ML models), as long as the accompanying model metadata is stored in a way that allows for easy retrieval and traceability.
