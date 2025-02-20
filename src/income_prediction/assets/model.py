import dagster as dg
import mlflow.pyfunc
import pandas as pd

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.resources.mlflow_session import MlflowSession


class ModelVersion(dg.ConfigurableResource):
    version: str
    uri: str


# FIXME: The explicit dependency on the model asset is not needed, but makes for a nicer graph in the UI
#        Ideally, we could depend on the `model` asset group instead
@dg.asset(group_name="evaluation", deps=["income_prediction_model_xgboost"])
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
