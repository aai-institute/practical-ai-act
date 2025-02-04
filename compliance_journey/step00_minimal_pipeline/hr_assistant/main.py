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

MODEL_URI = "runs:/d9eb179e44324ecc9446b51e612f78c7/asec_model"
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
    prediction = model.predict(data).tolist()

    # This is the only way to do this, thanks sklearn
    label_map = {0: "<=50k", 1: ">50k"}
    original_labels = [label_map[val] for val in prediction]
    return original_labels