---
tags:
    - Art. 13
    - Art. 14
    - Art. 15
---

# Experiment tracking

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"
    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation), in particular:
        - |Annex IV(3)|: Documentation of accuracy measures on a reference dataset as an expected level of accuracy
    - |Art. 13(3)(b)(ii)|, |Art. 15(3)| experiment tracking captures used performance metrics and levels of accuracy
    - |Art. 14(4)(a)|, understand the limitation of the underlying model by
            interpreting performance on reference data

## Motivation

AI models are typically trained on large amounts of data, using lots of compute resources.
The outputs that a trained model generates depend on many factors, like which version of a dataset was used (for more information, refer to the [data versioning](data-governance/data-versioning.md) section),
what configurable attributes (also called _hyperparameters_) were used for the training, but also training techniques used like batching, which optimization target, and many more.

The sum of all choices for the training of an AI model is often called an **experiment**.
Consequently, with so many moving parts and choices in an experiment, extensive documentation is needed to make training workflows transparent to practitioners, decision makers, and users alike.
A lot of ML/AI projects therefore use some form of _experiment tracking_ solution to help with visualizing experiments, evaluate model performance, and compare the performance in different experiments.

## Implementation notes

A vital aspect of experiment tracking software is to diligently mark the outputs (_artifacts_) of your training workflows to ensure reproducibility and a good overview on the situation.
This typically includes, but is not limited to,

-   versions of training and evaluation data, either raw or pre-processed, ideally in conjunction with data versioning,
-   hyperparameters giving as much information as possible in order to accurately reproduce experiments across platforms,
-   metrics and statistics giving information about the performance of the newly trained model.

## Key technologies

-   [MLflow](https://mlflow.org/)

    MLflow is an open-source experiment tracking platform that stores data and model artifacts, (hyper)parameters, and visualizes model performance in different stages of the ML training lifecycle.
    It features a number of pre-configured tracking plugins for popular machine learning libraries called **autologgers**, which allow the collection of metrics and configuration with minimal setup.
    In addition, MLflow comes with a UI that can be used to visualize metadata and results across experiments.

-   [Weights & Biases](https://wandb.ai/)

    Weights & Biases (or WandB) is a managed service for experiment tracking, metrics and metadata logging, and storing model and data artifacts.

-   [neptune.ai](https://neptune.ai)

    neptune.ai is another managed experiment tracking service for logging, visualizing, and monitoring metrics both in a training run and across multiple runs.
    It supports both managed and on-premise deployments, and offers special functionality for large language models (LLMs).

-   [ClearML](https://clear.ml/docs/)

    ClearML is an open-source experiment tracking and orchestration platform that allows for the management of experiments, data, and models.
    It features a web-based UI for visualizing metrics and metadata, and supports integration with popular machine learning libraries.

-   [Comet](https://www.comet.com/)

    Comet offers a managed experiment tracking service that allows for the logging and visualization of metrics, hyperparameters, and artifacts.
    It features a web-based UI for visualizing metrics and metadata, and supports integration with popular machine learning libraries.
