import dagster as dg

from .assets.model import model_container
from .assets.monitoring import nannyml_container

model_container_job = dg.define_asset_job(
    name="model_container_job",
    description="Inference service container image build",
    selection=[model_container],
)

nannyml_container_job = dg.define_asset_job(
    name="nannyml_container_job",
    description="Monitoring service container image build",
    selection=[nannyml_container],
)
