"""Data and model pipeline for the CPS ASEC income predictor."""

import typing
import mlflow
import sklearn.pipeline

if typing.TYPE_CHECKING:
    # Work around lazy imports in mlflow main module
    import mlflow.sklearn


# TODO: Adjust to actual paths in code.
CONFIG = {
    "paths": {
        "raw_data": "data/raw/",
        "clean_data": "data/clean/",
        "model": "models/",
    },
    "mlflow": {
        "tracking_uri": "http://localhost:5000",
        "experiment_name": "cps_asec",
    }
}


def setup_mlflow():
    mlflow.set_tracking_uri(CONFIG["mlflow"]["tracking_uri"])
    mlflow.set_experiment("cps_asec")
    mlflow.sklearn.autolog()


def cps_asec_model():
    # TODO(nicholasjng): Add steps.
    p = sklearn.pipeline.Pipeline([])
    return p
