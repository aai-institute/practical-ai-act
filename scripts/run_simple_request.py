from requests import post, get

model_input = {'age': 21,
               'workclass': 'Private',
               'fnlwgt': 192572,
               'education': 'HS-grad',
               'education-num': 9,
               'marital-status': 'Never-married',
               'occupation': 'Adm-clerical',
               'relationship': 'Own-child',
               'race': 'White',
               'sex': 'Female',
               'capital-gain': 0,
               'capital-loss': 0,
               'hours-per-week': 45,
               'native-country': 'United-States'}

response = post("http://localhost:8000/model/predict", json=model_input)
print(response.text)