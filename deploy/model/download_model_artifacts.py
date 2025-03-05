import os

import mlflow

model_name = os.getenv("MODEL_NAME")
version = os.getenv("MODEL_VERSION")
tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

print(f"Downloading model artifacts for {model_name}, version {version}")
print(f"MLflow tracking URL: {tracking_uri}")

client = mlflow.MlflowClient(tracking_uri=tracking_uri, registry_uri=tracking_uri)
if version == "latest":
    version = client.get_latest_versions(model_name)[0].version
    print(f"Resolved 'latest' to version {version}")

download_uri = client.get_model_version_download_uri(model_name, version)
mlflow.artifacts.download_artifacts(artifact_uri=download_uri, dst_path="/")
