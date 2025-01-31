import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from adult.data import AdultData

from compliance_journey.step00_minimal_pipeline.asec.preprocessing import (
    MappedColumn, WorkClass, Occupation, Race, RelationShip,
    MaritalStatus, Education, NativeCountry, TakeColumn, default_preprocessing
)

def test_mapped_column():
    df = pd.DataFrame({"col": ["A", "B", "C"]})
    mapping = {"A": 1, "B": 2, "C": 3}
    transformer = MappedColumn("col", mapping)
    transformed = transformer.fit_transform(df)
    expected = pd.Series([1, 2, 3], name="col").to_frame()
    pd.testing.assert_frame_equal(transformed, expected)

def test_take_column():
    df = pd.DataFrame({"col": [1, 2, 3]})
    transformer = TakeColumn("col")
    transformed = transformer.fit_transform(df)
    expected = pd.DataFrame({"col": [1, 2, 3]})
    np.testing.assert_array_equal(transformed, expected)


def test_workclass():
    values = ["Private", "?", "Self-emp-inc"]
    df = pd.DataFrame({AdultData.Column.WORK_CLASS: values})
    transformer = WorkClass()
    transformed = transformer.fit_transform(df)

    expected = np.zeros((3, 5))
    for row_idx, val in enumerate(values):
        col_index = transformer.categories[0].index(transformer.WORKCLASS_MAPPING[val])
        expected[row_idx, col_index] = 1

    np.testing.assert_array_equal(transformed.todense(), expected)



def test_occupation():
    df = pd.DataFrame({AdultData.Column.OCCUPATION: ["Exec-managerial", "?", "Handlers-cleaners"]})
    transformer = Occupation()
    transformed = transformer.fit_transform(df)

def test_race():
    df = pd.DataFrame({AdultData.Column.RACE: ["White", "Black", "Asian-Pac-Islander"]})
    transformer = Race()
    transformed = transformer.fit_transform(df)

def test_relationship():
    df = pd.DataFrame({AdultData.Column.RELATIONSHIP: ["Wife", "Own-Child", "Not-in-family"]})
    transformer = RelationShip()
    transformed = transformer.fit_transform(df)

def test_marital_status():
    df = pd.DataFrame({AdultData.Column.RELATIONSHIP: ["Married-civ-spouse", "Divorced", "Never-married"]})
    transformer = MaritalStatus()
    transformed = transformer.fit_transform(df)

def test_education():
    df = pd.DataFrame({AdultData.Column.EDUCATION: ["HS-grad", "Masters", "9th"]})
    transformer = Education()
    transformed = transformer.fit_transform(df)

def test_native_country():
    df = pd.DataFrame({AdultData.Column.NATIVE_COUNTRY: ["United-States", "India", "?"]})
    transformer = NativeCountry()
    transformed = transformer.fit_transform(df)

    #values =
    #expected = np.zeros((3, 5))
    #for row_idx, val in enumerate(values):
    #    col_index = transformer.categories[0].index(transformer.WORKCLASS_MAPPING[val])
    #    expected[row_idx, col_index] = 1

    #np.testing.assert_array_equal()


def test_default_preprocessing():
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
    transformed = default_preprocessing.fit_transform(df)
    assert transformed.shape[0] == df.shape[0]
