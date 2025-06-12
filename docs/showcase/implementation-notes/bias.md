# Bias Detection and Mitigation

!!! note

    While the dataset used in the showcase system contains multiple protected characteristics in the context of employment access (e.g., race, sex, age, disability status, ...), the implementation focuses on detecting and mitigating bias related to sex for demonstration purposes.

    Setting appropriate thresholds and metrics for detection of unacceptable bias is a complex task that requires careful consideration of the specific context and the potential impact of the model's predictions.

## Bias Detection

Two main types of bias are considered in the showcase system:

-   bias inherent to the dataset, which refers to the potential biases present in the training data that can lead to unfair predictions;
-   bias stemming from the ML model, which refers to the potential biases introduced by the model itself during training or inference.

Various metrics are calculated to assess the fairness of the model's predictions.
These metrics are logged to the MLflow experiment log during training, in order to be able to assess the model's fairness across different versions.

Two Python packages are used to calculate the relevant metrics:

-   [Fairlearn](https://fairlearn.org/): a toolkit for assessing and mitigating unfairness in machine learning models.
-   [AIF360](https://aif360.res.ibm.com/): a comprehensive toolkit for detecting and mitigating bias in AI systems.

## Bias Mitigation

TODO
