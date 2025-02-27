import dagster as dg

from .assets.model import model_container

model_container_job = dg.define_asset_job(
    name="model_container_job",
    description="Inference service container image build",
    selection=[model_container],
)
