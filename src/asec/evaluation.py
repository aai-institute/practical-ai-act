from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


@dataclass
class ClassificationEvaluationParams:
    test_size: float
    random_seed: int
    binary_positive_class: Any | None = None


@dataclass
class MetricCollection:
    acc: float
    f1: float
    recall: float
    precision: float

    def to_df(self):
        return pd.DataFrame([self.__dict__])


@dataclass
class ClassificationEvaluationResult:
    input_example: pd.DataFrame
    tests_metrics: MetricCollection
    train_metrics: MetricCollection | None = None


class ClassificationEvaluation:
    def __init__(
        self,
        X,
        y,
        evaluation_params: ClassificationEvaluationParams,
        fit_models=True,
        average: str = "binary",
    ):
        self.average = average
        self.fit_models = fit_models
        self.input_data = X
        self.output_data = y
        self.evaluation_params = evaluation_params

    def evaluate(
        self, model: Pipeline, include_train_metrics=True
    ) -> ClassificationEvaluationResult:
        X_train, X_test, y_train, y_test = self.get_train_test_split()
        if self.fit_models:
            model.fit(X_train, y_train)

        input_column_names = model.feature_names_in_
        input_example = X_train.loc[[X_train.index[0]], input_column_names]
        y_test_predict = model.predict(X_test)
        test_metrics = self._compute_metric_collection(y_test_predict, y_test)

        train_metrics: MetricCollection | None = None
        if include_train_metrics:
            y_train_pred = model.predict(X_train)
            train_metrics = self._compute_metric_collection(y_train, y_train_pred)

        return ClassificationEvaluationResult(
            input_example, test_metrics, train_metrics=train_metrics
        )

    def _compute_metric_collection(self, y_pred, y_true) -> MetricCollection:
        if self.evaluation_params.binary_positive_class is not None:
            pos_label = self.evaluation_params.binary_positive_class
        else:
            pos_label = 1
        accuracy = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, pos_label=pos_label, average=self.average)
        recall = recall_score(y_true, y_pred, pos_label=pos_label, average=self.average)
        precision = precision_score(
            y_true, y_pred, pos_label=pos_label, average=self.average
        )
        return MetricCollection(accuracy, f1, recall, precision)

    def get_train_test_split(self):
        return train_test_split(
            self.input_data,
            self.output_data,
            test_size=self.evaluation_params.test_size,
            random_state=self.evaluation_params.random_seed,
        )

    def get_test_data(self):
        _, X_test, _, y_test = self.get_train_test_split()
        return X_test, y_test
