from fastapi import FastAPI, Request
import pandas as pd
import mlflow


app = FastAPI()


MODEL_URI = "runs:/2dc7d8653cff4a8ab4219bb7fcd97a7f/asec_model"
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
    return model.predict(data).tolist()