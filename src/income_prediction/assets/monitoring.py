import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

import dagster as dg
import nannyml as nml
import pandas as pd

from asec.data import CensusASECMetadata
from asec.model_factory import LabelEncodedClassifier
from asec.nannyml import build_reference_data
from income_prediction.resources.configuration import Config, NannyMLConfig
from income_prediction.resources.mlflow_session import MlflowSession
from income_prediction.types import ModelVersion
from income_prediction.utils.docker import build_container_image
from income_prediction.utils.mlflow import load_model


@dg.asset(io_manager_key="lakefs_io_manager", group_name="deployment")
def reference_dataset(
    mlflow_session: MlflowSession,
    optuna_search_xgb: ModelVersion,
    test_data: pd.DataFrame,
) -> pd.DataFrame:
    """Reference dataset for post-deployment performance monitoring

    Based on predictions of the model on the test dataset"""

    model = load_model(optuna_search_xgb)
    X_test = test_data.drop(columns=[CensusASECMetadata.TARGET])
    y_test = test_data[CensusASECMetadata.TARGET]

    encoder = None
    if isinstance(model.steps[-1][1], LabelEncodedClassifier):
        encoder = model.steps[-1][1].encoder

    df = build_reference_data(model, X_test, y_test, encoder=encoder)
    return df


@dg.asset(group_name="deployment")
def nannyml_estimator(
    reference_dataset: pd.DataFrame,
    experiment_config: Config,
    nanny_ml_config: NannyMLConfig,
):
    estimator = nml.CBPE(
        problem_type="classification_multiclass",
        y_pred_proba={
            idx: f"prob_{idx}"
            for idx in range(
                len(experiment_config.salary_bands) + 1
            )  # Account for implicit highest band
        },
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
