from time import perf_counter

from requests import post

from asec.data import AdultData
from config import FILE_NAME_ADULT

adult_data = AdultData(FILE_NAME_ADULT)
X, _ = adult_data.load_input_output_data()

batch_df = X.dropna().sample(n=1000)
batch_df[AdultData.Column.HOURS_PER_WEEK] *= 2
batch = batch_df.to_dict(orient="records")

for record in batch:
    response = post("http://localhost:8000/model/predict", json=record)
    response.raise_for_status()