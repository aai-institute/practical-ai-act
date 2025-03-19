from pathlib import Path

import pandas as pd
import requests
import tqdm

X = pd.read_csv(
    Path(__file__).parents[1] / "data" / "test_data.csv",
    index_col=[0, 1],
)

batch_df = X.dropna().drop(columns=["SALARY_BAND"]).sample(n=100)
batch = batch_df.to_dict(orient="records")

predict_endpoint = "http://localhost:8001/model/predict"

# Batch request
response = requests.post(predict_endpoint, json=batch)
response.raise_for_status()
print("Batch request ID:", response.headers["X-Request-ID"])

# Single-record requests
with tqdm.tqdm(total=len(batch)) as pbar:
    for record in batch:
        response = requests.post(predict_endpoint, json=record)
        response.raise_for_status()
        pbar.update(1)
