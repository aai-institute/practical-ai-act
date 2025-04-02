import logging
import os
from tempfile import TemporaryDirectory

import mlflow
import pandas as pd
from mlflow.models import infer_signature
from mlflow.models.model import ModelInfo
from sklearn.pipeline import Pipeline

from asec.evaluation import ClassificationEvaluationResult


def mlflow_track(
    model: Pipeline,
    result: ClassificationEvaluationResult,
    experiment_name: str,
    model_name: str,
    artifact_path: str,
    reference_data: pd.DataFrame | None = None,
    tags: dict[str, str] = None,
) -> ModelInfo:
    test_metrics = result.tests_metrics

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        mlflow.log_metric("accuracy", test_metrics.acc)
        mlflow.log_metric("f1", test_metrics.f1)
        mlflow.log_metric("recall", test_metrics.recall)
        mlflow.log_metric("precision", test_metrics.precision)

        if reference_data is not None:
            with TemporaryDirectory() as tmpdir:
                ref_data_path = os.path.join(tmpdir, "reference_data.parquet")
                reference_data.to_parquet(ref_data_path)
                mlflow.log_artifact(ref_data_path)

        if tags is not None:
            for key, val in tags.items():
                mlflow.set_tag(key, val)

        signature = infer_signature(
            result.input_example, model.predict(result.input_example)
        )

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=artifact_path,
            signature=signature,
            input_example=result.input_example,
            registered_model_name=model_name,
        )
        logging.info(f"Registered {str(model_info)}")
        return model_info
