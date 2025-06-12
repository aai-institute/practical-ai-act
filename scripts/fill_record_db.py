import pandas as pd
import requests
import tqdm

# Test data set from lakeFS repository
X = pd.read_parquet("lakefs://twai-pipeline/main/data/test_data.parquet")

batch_df = X.dropna().sample(n=100)
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
