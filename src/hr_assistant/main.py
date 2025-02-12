from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TypedDict

import mlflow
from fastapi import FastAPI, Request, Response

from .api.info import router as info_router
from .api.predict import router as predict_router
from .config import MODEL_URI
from .dependencies.logging import PredictionLogger, SQLitePredictionLogger


def _load_model(model_uri: str) -> mlflow.sklearn.Model:
    return mlflow.sklearn.load_model("models:/xgboost-classifier/latest")


class State(TypedDict):
    model: mlflow.sklearn.Model
    request_logger: PredictionLogger


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    logger = SQLitePredictionLogger(
        "predictions.sqlite3", table_name="predictions", capacity=100
    )

    yield {
        "model": _load_model(MODEL_URI),
        "request_logger": logger,
    }

    logger.flush()


app = FastAPI(lifespan=lifespan)

app.include_router(predict_router, prefix="/model")
app.include_router(info_router, prefix="/model")


@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"Request: {request.url.path}")

    response: Response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response
