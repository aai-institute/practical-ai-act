# Use-case Description

!!! warning

    This is a fictional use case created solely for demonstration and educational purposes.
    It is not a real deployment and should not be interpreted as a commercial or operational system.
    It does not represent any real recruitment system or policy and should not be used for making real-world hiring decisions.

## Purpose

This AI system is designed to assist recruiters and hiring
managers in the recruitment process by automatically predicting salary bands
for job candidates, so helping to streamline candidate filtering and matching.

## Functionality

-   Uses a classification model trained on publicly available [data](#data) to
    predict salary bands based on provided candidate's features.
-   Exposes the model through a web API

## Data

The classifier is trained on [US Census CPS ASEC dataset](https://www2.census.gov/programs-surveys/cps/datasets/)

**Reading**:

-   [Retiring Adult: New Datasets for Fair Machine Learning](https://arxiv.org/pdf/2108.04884)

**Resources**:

-   [folktables](https://github.com/socialfoundations/folktables)
