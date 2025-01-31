import os
from pathlib import Path

from fastapi import FastAPI, Request
from pydantic import BaseModel, conint, PositiveFloat
import pandas as pd
import mlflow

from config import MLFLOW_SUBFOLDER

# class PredictionInput(BaseModel):
#    A_AGE: conint(ge=16)
#    HRSWK: PositiveFloat
#    FNLWGT: PositiveFloat


app = FastAPI()

# MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
# MODEL_URI = os.getenv("MODEL_URI", "models:/my_model/Production")

MODEL_URI = "runs:/f8c2ee138df645e7a3a0a8b29510361b/asec_model"
MLFLOW_TRACKING_URI = "/Users/kristof/Projects/twai-pipeline/compliance_journey/step00_minimal_pipeline/mlruns"
print(MLFLOW_TRACKING_URI)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model = mlflow.sklearn.load_model(MODEL_URI)


@app.get("/info/")
def model_info():
    return str(model)


@app.post("/predict/")
async def predict(request: Request):
    data = pd.DataFrame.from_records([await request.json()])
    prediction = model.predict(data)
    return prediction.tolist()
