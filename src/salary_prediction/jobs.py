import dagster as dg

from .assets.model import model_container
from .assets.monitoring import nannyml_container, nannyml_estimator, reference_dataset

model_container_job = dg.define_asset_job(
    name="model_container_job",
    description="Inference service container image build",
    selection=[model_container],
)

nannyml_container_job = dg.define_asset_job(
    name="nannyml_container_job",
    description="Monitoring service container image build",
    selection=[reference_dataset, nannyml_estimator, nannyml_container],
)

e2e_pipeline_job = dg.define_asset_job(
    name="e2e_pipeline_job",
    description="End-to-end model training pipeline job",
    selection=dg.AssetSelection.groups().all(),
)
