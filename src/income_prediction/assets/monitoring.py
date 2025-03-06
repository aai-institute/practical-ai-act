from pathlib import Path
import dagster as dg

from income_prediction.assets.model import ModelVersion
from income_prediction.utils.docker import build_container_image


@dg.asset(kinds={"docker"}, group_name="deployment")
def nannyml_container(context: dg.AssetExecutionContext, model_version: ModelVersion):
    build_context = Path(__file__).parents[3] / "deploy" / "nannyml"
    image_tag = f"nannyml:latest"
    build_result = build_container_image(build_context, [image_tag])

    if not build_result.success:
        context.log.info("Container build logs:\n" + build_result.build_logs)
        raise ValueError(f"Failed to build container image: {build_result.build_logs}")

    return dg.Output(
        value=image_tag,
        metadata={
            "image_tag": image_tag,
            "image_name": build_result.image_name,
            "image_digest": build_result.image_digest,
            "build_logs": dg.MetadataValue.text(build_result.build_logs),
        },
    )
