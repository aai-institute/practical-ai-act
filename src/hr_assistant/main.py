from contextlib import asynccontextmanager
from pathlib import Path

import mlflow
import mlflow.pyfunc
from fastapi import FastAPI

from hr_assistant import api, dependencies

PREDICTION_LOG_PATH = Path("predictions.jsonl")

# FIXME: Parameterize the model name and version
MLFLOW_MODEL_NAME = "tracking-quickstart"
MLFLOW_MODEL_VERSION = 1


def _load_model(model_name: str, model_version: int) -> mlflow.pyfunc.PyFuncModel:
    return mlflow.pyfunc.load_model(f"models:/{model_name}/{model_version}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make a singleton prediction logger instance available to the application
    # logger = dependencies.logging.PredictionLogger(PREDICTION_LOG_PATH)
    # logger = dependencies.logging.OpenSearchPredictionLogger(
    #     "https://localhost:9200", "predictions"
    # )
    logger = dependencies.logging.DuckDBPredictionLogger(
        Path("predictions.db"), "predictions"
    )
    app.state.request_logger = logger

    app.state.model = _load_model(MLFLOW_MODEL_NAME, MLFLOW_MODEL_VERSION)

    yield

    # Ensure the logger buffer is flushed before the application exits or restarts
    logger.flush()


app = FastAPI(lifespan=lifespan)

app.include_router(api.predict, prefix="/model")
