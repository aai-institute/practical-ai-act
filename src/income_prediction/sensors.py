import dagster as dg

from . import MlflowSession
from .jobs import model_container_job, nannyml_container_job
from .types import ModelVersion


# TODO: This sensor can be removed once the pipeline is transformed
@dg.sensor(
    jobs=[model_container_job, nannyml_container_job],
    description="Build inference server container image whenever a new model version is registered in the MLflow registry",
    default_status=dg.DefaultSensorStatus.STOPPED,
)
def model_version_trigger(context, mlflow_session: MlflowSession):
    model_name = "xgboost-classifier"
    ver, uri = mlflow_session.get_latest_model_version(model_name)
    if context.cursor != ver:
        model_container_request = dg.RunRequest(
            run_key=f"model-container-build-{model_name}-{ver}",
            run_config={
                "resources": {
                    "model_version": {
                        "config": ModelVersion(version=ver, uri=uri).model_dump(),
                    }
                },
            },
            tags={"model_version": ver, "model_uri": uri},
            job_name=model_container_job.name,
        )
        nannyml_container_request = dg.RunRequest(
            run_key=f"model-nannyml-build-{model_name}-{ver}",
            run_config={
                "resources": {
                    "model_version": {
                        "config": ModelVersion(version=ver, uri=uri).model_dump(),
                    }
                },
            },
            tags={"model_version": ver, "model_uri": uri},
            job_name=nannyml_container_job.name,
        )

        yield model_container_request
        yield nannyml_container_request

        context.update_cursor(ver)
