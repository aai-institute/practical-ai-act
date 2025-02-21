import dagster as dg
import pandas as pd

from . import InferenceLog, MlflowSession
from .assets.model import ModelVersion
from .jobs import data_quality_report, model_evaluation_job, model_container_job


def _need_to_run(log_df: pd.DataFrame, cursor: str | None) -> bool:
    if cursor is None:
        return True
    if log_df.empty:
        return False
    return log_df.iloc[-1].id != cursor


@dg.sensor(
    job=data_quality_report,
    minimum_interval_seconds=10,
    default_status=dg.DefaultSensorStatus.STOPPED,
)
def report_trigger(context: dg.SensorEvaluationContext, inference_logs: InferenceLog):
    log = inference_logs.fetch_inference_log()
    last_id = context.cursor

    context.log.info(f"Log info: {log.info}, last ID: {last_id}")

    if _need_to_run(log, last_id):
        last_id = log.iloc[-1].id
        yield dg.RunRequest(
            run_key=f"report-{last_id}",
        )
        context.update_cursor(last_id)
    else:
        yield dg.SkipReason("No new inference data")


@dg.sensor(
    jobs=[model_evaluation_job, model_container_job],
    default_status=dg.DefaultSensorStatus.STOPPED,
)
def model_version_trigger(context, mlflow_session: MlflowSession):
    model_name = "xgboost-classifier"
    ver, uri = mlflow_session.get_latest_model_version(model_name)
    if context.cursor != ver:
        yield dg.RunRequest(
            run_key=f"evaluate-{model_name}-{ver}",
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
