import os

import mlflow

model_uri = os.getenv("MODEL_URI")
print(f"Downloading model artifacts from {model_uri}")
print(f"MLflow tracking URL: {os.getenv('MLFLOW_TRACKING_URI')}")

# Download the model artifacts
model_info = mlflow.models.get_model_info(model_uri)

client = mlflow.MlflowClient()
client.download_artifacts(model_info.run_id, model_info.artifact_path, "/")
