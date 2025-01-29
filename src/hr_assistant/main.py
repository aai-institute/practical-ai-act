from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from hr_assistant import api, dependencies

PREDICTION_LOG_PATH = Path("predictions.jsonl")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make a singleton prediction logger instance available to the application
    logger = dependencies.logging.PredictionLogger(PREDICTION_LOG_PATH)
    app.state.request_logger = logger

    yield

    # Ensure the logger buffer is flushed before the application exits or restarts
    logger._buffer.flush()


app = FastAPI(lifespan=lifespan)

app.include_router(api.predict, prefix="/model")
