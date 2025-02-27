from pathlib import Path

import dagster as dg
import mlflow.pyfunc
import pandas as pd

from asec.data import CensusASECMetadata
from income_prediction.resources.mlflow_session import MlflowSession
from income_prediction.utils.docker import build_container_image


class ModelVersion(dg.ConfigurableResource):
    version: str
    uri: str


# FIXME: The explicit dependency on the model asset is not needed, but makes for a nicer graph in the UI
#        Ideally, we could depend on the `model` asset group instead
@dg.asset(group_name="evaluation", deps=["optuna_search_xgb"])
def model_evaluation(
    context: dg.AssetExecutionContext,
    model_version: ModelVersion,
    test_data: pd.DataFrame,
    mlflow_session: MlflowSession,
) -> None:
    context.log.info(
        f"Evaluating model version {model_version.version} at {model_version.uri}"
    )

    # FIXME: This logs to a different run than the model training. Not great.
    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name="performance_evaluation"):
            model = mlflow.pyfunc.load_model(model_version.uri)
            mlflow.evaluate(
                model=model.predict,
                data=test_data,
                targets=CensusASECMetadata.TARGET,
                model_type="classifier",
            )


@dg.asset(kinds={"docker"}, group_name="deployment")
def model_container(context: dg.AssetExecutionContext, model_version: ModelVersion):
    context.log.info(f"Building container for model version {model_version.version}")

    build_context = Path(__file__).parents[3] / "deploy" / "model"
    context.log.info(f"Build context: {build_context}")
    image_tag = f"xgboost-classifier:{model_version.version}"

    build_result = build_container_image(build_context, [image_tag])

    if not build_result.success:
        context.log.info("Container build logs:\n" + build_result.build_logs)
        raise ValueError("Failed to build container image")

    return dg.Output(
        value=image_tag,
        metadata={
            "image_tag": image_tag,
            "image_name": build_result.image_name,
            "image_digest": build_result.image_digest,
            "build_logs": dg.MetadataValue.text(build_result.build_logs),
        },
    )
