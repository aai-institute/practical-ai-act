# Model Monitoring

## Model Performance Estimation

The NannyML library implements two approaches to model performance estimation:

-   _Confidence-based performance estimation_ (CBPE) for [binary](https://nannyml.readthedocs.io/en/stable/tutorials/performance_estimation/binary_performance_estimation.html) and [multiclass](https://nannyml.readthedocs.io/en/stable/tutorials/performance_estimation/multiclass_performance_estimation.html) classification tasks
-   _Direct Loss Estimation_ (DLE) for [regression](https://nannyml.readthedocs.io/en/stable/tutorials/performance_estimation/regression_performance_estimation.html) tasks

Since the ML problem for the showcase is a classification task, the CBPE approach is applied.

## Data Drift Detection

NannyML implements a variety of data drift detection algorithms for [univariate](https://nannyml.readthedocs.io/en/stable/tutorials/detecting_data_drift/univariate_drift_detection.html) and [multivariate](https://nannyml.readthedocs.io/en/stable/tutorials/detecting_data_drift/multivariate_drift_detection.html) data.

TODO: How do we use the data drift detection algorithms in the showcase?

## Reporting

Both model performance estimation and data drift detection algorithm in NannyML operate on _chunks_ of model predictions.
Therefore, it is straightforward to generate periodic reports on the model's performance as part of a monitoring workflow.

The showcase implements a simple reporting mechanism that builds a containerized monitoring dashboard of the reported performance metrics based on the prediction stored in the [inference log](inference-logging.md).

Similarly, these reports could be implemented as a scheduled workflow that generates reports on a daily, weekly, or monthly basis.
