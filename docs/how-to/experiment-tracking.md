# Data versioning

!!! success "Compliance Info"
    TODO: Add article references to provisions addressed by experiment tracking

## Motivation

AI models are typically trained on large amounts of data, using lots of compute resources.
The outputs that a trained model generates depend on many factors, like which version of a dataset was used (for more information, refer to the [data versioning](data-versioning.md) section),
what configurable attributes (also called *hyperparameters*) were used for the training, but also training techniques used like batching, which optimization target, and many more.

The sum of all choices for the training of an AI model is often called an **experiment**.
Consequently, with so many moving parts and choices in an experiment, extensive documentation is needed to make training workflows transparent to practitioners, decision makers, and users alike.
A lot of ML/AI projects therefore use some form of *experiment tracking* solution to help with visualizing experiments, evaluate model performance, and compare the performance in different experiments.

## Implementation notes

A vital aspect of experiment tracking software is to diligently mark the outputs (*artifacts*) of your training workflows to ensure reproducibility and a good overview on the situation.
This typically includes, but is not limited to,

* versions of training and evaluation data, either raw or pre-processed, ideally in conjunction with data versioning,
* hyperparameters giving as much information as possible in order to accurately reproduce experiments across platforms,
* metrics and statistics giving information about the performance of the newly trained model.

## Key technologies

1. [MLflow](https://mlflow.org/)

MLflow is an open-source experiment tracking platform that stores data and model artifacts, (hyper)parameters, and visualizes model performance in different stages of the ML training lifecycle.
It features a number of pre-configured tracking plugins for popular machine learning libraries called **autologgers**, which allow the collection of metrics and configuration with minimal setup.
In addition, MLflow comes with a UI that can be used to visualize metadata and results across experiments.
