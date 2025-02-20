import dagster as dg
import pandas as pd

from income_prediction.resources.monitoring import InferenceLog


@dg.asset
def nannyml_report(
    context: dg.AssetExecutionContext,
    reference_dataset: pd.DataFrame,
    inference_logs: InferenceLog,
) -> None:
    log_df = inference_logs.fetch_inference_log()
    context.log.info(
        f"Generating NannyML report, reference dataset:\n{reference_dataset.shape},\ninference logs:\n{log_df.shape}"
    )
