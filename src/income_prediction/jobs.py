import dagster as dg

from .assets import nannyml_report, model_evaluation


data_quality_report = dg.define_asset_job(
    name="data_quality_report",
    description="Data quality and model performance report",
    selection=[nannyml_report],
)

model_evaluation_job = dg.define_asset_job(
    name="model_evaluation_job",
    description="Model performance evaluation",
    selection=[model_evaluation],
)
