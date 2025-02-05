from fastapi import FastAPI, Request
import pandas as pd
import mlflow


app = FastAPI()


MODEL_URI = "runs:/24581578617d4fbca2e153ac070271b8/asec_model"
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
