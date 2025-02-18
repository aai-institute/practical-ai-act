from pathlib import Path

from more_itertools import take
import pandas as pd
from requests import post
import tqdm


X = pd.read_csv(
    Path(__file__).parents[1] / "data" / "test_data.csv",
    index_col=[0, 1],
)

batch_df = X.dropna().drop(columns=["SALARY_BAND"]).sample(n=1000)
batch = batch_df.to_dict(orient="records")

# Batch request
response = post("http://localhost:8000/model/predict", json=batch)
response.raise_for_status()

# Single-record requests
with tqdm.tqdm(total=len(batch)) as pbar:
    for record in batch:
        response = post("http://localhost:8000/model/predict", json=record)
        response.raise_for_status()
        pbar.update(1)
