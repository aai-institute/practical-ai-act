import pandas as pd
from compliance_journey.step00_minimal_pipeline.asec.features import collect_features

def test_collect_features():
    record = {'age': 21,
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
    df = pd.DataFrame.from_records([record])
    feature_union= collect_features()

    transformed = feature_union.fit_transform(df)
    assert transformed.shape[0] == df.shape[0]