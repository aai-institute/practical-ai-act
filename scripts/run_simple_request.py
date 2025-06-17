from requests import post

model_input = {
    "SEX": 1,
    "SCH": 1,
    "MAR": 3,
    "RAC1P": 1,
    "CIT": 1,
    "DIS": 2,
    "COW": 4,
    "INDP": 9470,
    "WKL": 1,
    "OCCP": 2100,
    "HICOV": 1,
    "WKWN": 52,
    "WKHP": 40,
    "AGEP": 52,
    "SCHL": 21,
}

response = post("http://localhost:8001/model/predict", json=model_input)
print("Request ID:", response.headers["X-Request-ID"])
print(response.text)
