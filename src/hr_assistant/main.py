import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

from .api.info import router as info_router
from .api.predict import router as predict_router

# Prometheus metrics exporter
instrumentator = Instrumentator()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator:
    instrumentator.expose(app, tags=["monitoring"])
    yield


app = FastAPI(lifespan=lifespan)
instrumentator.instrument(app)

app.include_router(predict_router, prefix="/model")
app.include_router(info_router, prefix="/model")


def _make_request_id() -> str:
    return str(uuid.uuid4())


@app.middleware("http")
async def generate_request_id(request: Request, call_next):
    """Add a unique request ID to each request and its response headers"""
    request_id = _make_request_id()
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
