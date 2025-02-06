from contextlib import asynccontextmanager
from fastapi import FastAPI
import mlflow

from hr_assistant_app import api


MODEL_URI = "runs:/a62dbc9aff7040598b9b1b66d9b786f3/asec_model"
MLFLOW_TRACKING_URI = "/Users/kristof/Projects/twai-pipeline/compliance_journey/step00_minimal_pipeline/mlruns"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def _load_model(model_uri: str) -> mlflow.sklearn.Model:
    return mlflow.sklearn.load_model(model_uri)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = _load_model(MODEL_URI)
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(api.predict_router, prefix="/model")
app.include_router(api.info_router, prefix="model")

