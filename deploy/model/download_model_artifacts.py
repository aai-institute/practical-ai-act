import os
import typing

import mlflow
import mlflow.artifacts
import mlflow.entities

if typing.TYPE_CHECKING:
    import mlflow.artifacts


def _find_explainer_output(
    client: mlflow.MlflowClient, run: mlflow.entities.Run
) -> mlflow.entities.LoggedModel:
    for output in run.outputs.model_outputs:
        logged_model = client.get_logged_model(output.model_id)
        if logged_model.name == "explainer":
            return client.get_logged_model(output.model_id)
    raise ValueError("No 'explain' output found in the model outputs.")


model_name = os.getenv("MODEL_NAME")
version = os.getenv("MODEL_VERSION", "latest")
tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

if not model_name:
    raise ValueError("MODEL_NAME environment variable is not set.")

print(f"Downloading model artifacts for {model_name!r}, version {version!r}")
print(f"MLflow tracking URL: {tracking_uri}")

client = mlflow.MlflowClient(tracking_uri=tracking_uri, registry_uri=tracking_uri)
if version == "latest":
    version = client.get_latest_versions(model_name)[0].version
    print(f"Resolved 'latest' to version {version}")

model_version = client.get_model_version(model_name, version)
print(f"Model version details: {model_version}")

model_artifact_uri = client.get_model_version_download_uri(model_name, version)
mlflow.artifacts.download_artifacts(artifact_uri=model_artifact_uri, dst_path="/model")

explainer_model = _find_explainer_output(client, client.get_run(model_version.run_id))
explainer_artifact_uri = explainer_model.artifact_location
mlflow.artifacts.download_artifacts(
    artifact_uri=explainer_artifact_uri, dst_path="/explainer"
)
