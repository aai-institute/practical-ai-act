from pathlib import Path

import dagster as dg

from income_prediction.utils.docker import build_container_image


class ModelVersion(dg.ConfigurableResource):
    version: str
    uri: str


@dg.asset(kinds={"docker"}, group_name="deployment")
def model_container(context: dg.AssetExecutionContext, model_version: ModelVersion):
    context.log.info(f"Building container for model version {model_version.version}")

    # Assumes a model URI of the form `models:/<model_name>/<version>``
    model_name = model_version.uri.rsplit("/")[-2]

    build_context = Path(__file__).parents[3] / "deploy" / "model"
    image_tags = [f"{model_name}:{suffix}" for suffix in [model_version.version, "latest"]]
    context.log.info(f"Build context: {build_context}")
    context.log.info(f"Image tags: {image_tags}")

    build_result = build_container_image(
        build_context,
        tags=image_tags,
        build_args={
            # FIXME: Hardcoded, but should be made configurable
            "MLFLOW_TRACKING_URI": "http://host.docker.internal:50000",
            "MODEL_NAME": model_name,
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
