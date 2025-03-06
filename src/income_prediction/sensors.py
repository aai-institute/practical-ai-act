import dagster as dg

from . import MlflowSession
from .assets.model import ModelVersion
from .jobs import model_container_job, nannyml_container_job


@dg.sensor(
    jobs=[model_container_job, nannyml_container_job],
    description="Build inference server container image whenever a new model version is registered in the MLflow registry",
    default_status=dg.DefaultSensorStatus.STOPPED,
)
def model_version_trigger(context, mlflow_session: MlflowSession):
    model_name = "xgboost-classifier"
    ver, uri = mlflow_session.get_latest_model_version(model_name)
    if context.cursor != ver:
        yield dg.RunRequest(
            run_key=f"model-container-build-{model_name}-{ver}",
            run_config={
                "resources": {
                    "model_version": {
                        "config": ModelVersion(version=ver, uri=uri).model_dump(),
                    }
                },
            },
            tags={"model_version": ver, "model_uri": uri},
        )
        context.update_cursor(ver)
