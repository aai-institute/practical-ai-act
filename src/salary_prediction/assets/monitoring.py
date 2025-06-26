import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

import dagster as dg
import mlflow
import nannyml as nml
import pandas as pd

from asec.data import PUMSMetaData
from salary_prediction.resources.configuration import NannyMLConfig
from salary_prediction.resources.mlflow_session import MlflowSession
from salary_prediction.types import ModelVersion
from salary_prediction.utils.docker import build_container_image
from salary_prediction.utils.nannyml import build_reference_data


@dg.asset(io_manager_key="lakefs_io_manager", group_name="deployment", kinds={"pandas"})
def reference_dataset(
    mlflow_session: MlflowSession,
    optuna_search_xgb: ModelVersion,
    test_data: pd.DataFrame,
) -> pd.DataFrame:
    """Reference dataset for post-deployment performance monitoring

    Based on predictions of the model on the test dataset"""

    model = mlflow.sklearn.load_model(optuna_search_xgb.version)
    X_test = test_data.drop(columns=[PUMSMetaData.TARGET])
    y_test = test_data[PUMSMetaData.TARGET]
    df = build_reference_data(model, X_test, y_test)
    return df


@dg.asset(group_name="deployment")
def nannyml_estimator(
    reference_dataset: pd.DataFrame,
    nanny_ml_config: NannyMLConfig,
):
    estimator = nml.CBPE(
        problem_type="classification_binary",
        y_pred_proba="prediction_probability",
        y_pred="prediction",
        y_true="target",
        metrics=nanny_ml_config.metrics,
        chunk_size=nanny_ml_config.chunk_size,
    )
    estimator.fit(reference_dataset)
    return estimator


@dg.asset(kinds={"docker"}, group_name="deployment")
def nannyml_container(
    context: dg.AssetExecutionContext,
    optuna_search_xgb: ModelVersion,
    nannyml_estimator: nml.CBPE,
) -> dg.Output:
    model_version = optuna_search_xgb
    build_context = Path(__file__).parents[3]
    image_tags = [f"nannyml:{suffix}" for suffix in [model_version.version, "latest"]]
    context.log.info(f"{image_tags=}")

    # Create tempfile inside the build context, so it can be copied into the image
    with NamedTemporaryFile(
        prefix="nannyml-cbpe-", suffix=".pkl", dir=build_context
    ) as tmp_file:
        pkl_path = Path(tmp_file.name)

        with open(pkl_path, "wb") as f:
            pickle.dump(nannyml_estimator, f)

        context.log.info(f"{pkl_path=}")
        context.log.info(f"{build_context=}")
        build_result = build_container_image(
            build_context,
            image_tags,
            build_args={"NANNYML_ESTIMATOR": str(pkl_path.name)},
            dockerfile_path=build_context / "deploy" / "nannyml" / "Dockerfile",
        )

    if not build_result.success:
        context.log.info("Container build logs:\n" + build_result.build_logs)
        raise ValueError(f"Failed to build container image: {build_result.build_logs}")

    return dg.Output(
        value=image_tags,
        metadata={
            "image_tags": image_tags,
            "image_name": build_result.image_name,
            "image_digest": build_result.image_digest,
            "build_logs": dg.MetadataValue.text(build_result.build_logs),
        },
    )
