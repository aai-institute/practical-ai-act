import pytest
import pandas as pd
from asec.features import (
    collect_features,
    MappedColumn,
)


@pytest.mark.parametrize(
    "original_values, mapping, expected, unknown_default",
    [
        (["A", "B", "C"], {"A": 1, "B": 2, "C": 3}, [1, 2, 3], None),
        (["A", "B", "D"], {"A": 1, "B": 2, "C": 3}, [1, 2, pd.NA], None),
        (["A", "B", "D"], {"A": 1, "B": 2, "C": 3}, [1, 2, "foo"], "foo"),
    ],
)
def test_mapped_column(original_values, mapping, expected, unknown_default):
    df = pd.DataFrame({"col": original_values})
    if unknown_default is None:
        transformer = MappedColumn("col", mapping=mapping)
    else:
        transformer = MappedColumn("col", mapping=mapping, unknown_default=unknown_default)
    transformed = transformer.fit_transform(df)
    expected = pd.Series(expected, name="col").to_frame()
    pd.testing.assert_frame_equal(transformed, expected)


def test_collect_features():
    record = {
        "age": 21,
        "workclass": "Private",
        "fnlwgt": 192572,
        "education": "HS-grad",
        "education-num": 9,
        "marital-status": "Never-married",
        "occupation": "Adm-clerical",
        "relationship": "Own-child",
        "race": "White",
        "sex": "Female",
        "capital-gain": 0,
        "capital-loss": 0,
        "hours-per-week": 45,
        "native-country": "United-States",
    }
    df = pd.DataFrame.from_records([record])
    feature_union = collect_features()

    transformed = feature_union.fit_transform(df)
    assert transformed.shape[0] == df.shape[0]
