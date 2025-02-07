from contextlib import asynccontextmanager

import mlflow
import mlflow.sklearn
from fastapi import FastAPI

from hr_assistant import api, dependencies
from hr_assistant.config import MLFLOW_MODEL_URI


def _load_model(model_uri: str) -> mlflow.sklearn.Model:
    # return mlflow.pyfunc.load_model(f"models:/{model_name}/{model_version}")
    return mlflow.sklearn.load_model(model_uri)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make a singleton prediction logger instance available to the application
    # logger = dependencies.logging.PredictionLogger(PREDICTION_LOG_PATH)
    # logger = dependencies.logging.OpenSearchPredictionLogger(
    #     "https://localhost:9200", "predictions"
    # )
    # logger = dependencies.logging.DuckDBPredictionLogger(
    #     Path("predictions.db"), "predictions"
    # )
    logger = dependencies.logging.SQLitePredictionLogger(
        "predictions.sqlite3", table_name="predictions", capacity=100
    )
    app.state.request_logger = logger

    app.state.model = _load_model(MLFLOW_MODEL_URI)

    yield

    # Ensure the logger buffer is flushed before the application exits or restarts
    logger.flush()


app = FastAPI(lifespan=lifespan)

app.include_router(api.predict, prefix="/model")
