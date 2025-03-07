import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

import dagster as dg
import pandas as pd
import sklearn.pipeline
import nannyml as nml

from asec.data import CensusASECMetadata
from asec.nannyml import build_reference_data
from income_prediction.resources.configuration import Config, NannyMLConfig
from income_prediction.assets.model import ModelVersion
from income_prediction.utils.docker import build_container_image


@dg.asset(io_manager_key="lakefs_io_manager", group_name="deployment", deps=["optuna_search_xgb", "test_data"])
def reference_dataset(
    optuna_search_xgb: sklearn.pipeline.Pipeline,
    test_data: pd.DataFrame,
) -> pd.DataFrame:
    """Reference dataset for post-deployment performance monitoring

    Based on predictions of the model on the test dataset"""

    model = optuna_search_xgb
    X_test = test_data.drop(columns=[CensusASECMetadata.TARGET])
    y_test = test_data[CensusASECMetadata.TARGET]

    df = build_reference_data(
        model, X_test, y_test, encoder=model.steps[-1][1].encoder
    )
    return df

@dg.asset(group_name="deployment", deps=["reference_dataset"])
def nannyml_estimator(reference_dataset: pd.DataFrame, config: Config, nanny_ml_config: NannyMLConfig):
    estimator = nml.CBPE(
        problem_type="classification_multiclass",
        y_pred_proba={
            idx: f"prob_{idx}"
            for idx in range(
                len(config.salary_bands) + 1
            )  # Account for implicit highest band
        },
        y_pred="prediction",
        y_true="target",
        metrics=nanny_ml_config.metrics,
        chunk_size=nanny_ml_config.chunk_size,
    )
    estimator.fit(reference_dataset)
    return estimator


@dg.asset(kinds={"docker"}, group_name="deployment", deps=["nannyml_estimator"])
def nannyml_container(context: dg.AssetExecutionContext, model_version: ModelVersion,
                      nannyml_estimator: nml.CBPE) -> dg.Output:
    build_context = Path(__file__).parents[3] / "deploy" / "nannyml"
    image_tag = f"nannyml:{model_version.version}"
    context.log.info(f"{image_tag=}")
    with NamedTemporaryFile(suffix=".pkl", delete=True, dir=build_context) as tmp_file:
        pkl_path = Path(tmp_file.name)

        with open(pkl_path, "wb") as f:
            pickle.dump(nannyml_estimator, f)

        context.log.info(f"{pkl_path=}")
        context.log.info(f"File exists: {pkl_path.exists()}")
        build_result = build_container_image(build_context,
                                             [image_tag],
                                             build_args={"NANNYML_ESTIMATOR": str(pkl_path.name)})

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


