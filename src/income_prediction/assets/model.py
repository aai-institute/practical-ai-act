from pathlib import Path

import dagster as dg

from income_prediction.utils.docker import build_container_image


class ModelVersion(dg.ConfigurableResource):
    version: str
    uri: str


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
