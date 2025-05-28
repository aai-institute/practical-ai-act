from pathlib import Path

import dagster as dg

from income_prediction.types import ModelVersion
from income_prediction.utils.docker import build_container_image


@dg.asset(kinds={"docker"}, group_name="deployment")
def model_container(context: dg.AssetExecutionContext, optuna_search_xgb: ModelVersion):
    model_version = optuna_search_xgb
    context.log.info(f"Building container for model version {model_version}")

    build_context = Path(__file__).parents[3] / "deploy" / "model"
    image_tags = [
        f"{model_version.name}:{suffix}" for suffix in [model_version.version, "latest"]
    ]
    context.log.info(f"Build context: {build_context}")
    context.log.info(f"Image tags: {image_tags}")

    build_result = build_container_image(
        build_context,
        tags=image_tags,
        network="host",
        build_args={
            # FIXME: Hardcoded based on Compose stack, but should be made configurable
            "MLFLOW_TRACKING_URI": "http://localhost:50000",
            "MODEL_NAME": model_version.name,
            "MODEL_VERSION": model_version.version,
        },
    )

    if not build_result.success:
        context.log.info("Container build logs:\n" + build_result.build_logs)
        raise ValueError("Failed to build container image", build_result.build_logs)

    return dg.Output(
        value=image_tags,
        metadata={
            "image_tags": image_tags,
            "image_name": build_result.image_name,
            "image_digest": build_result.image_digest,
            "build_logs": dg.MetadataValue.text(build_result.build_logs),
        },
    )
