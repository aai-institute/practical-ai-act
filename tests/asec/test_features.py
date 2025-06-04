import pandas as pd
import pytest

from asec.features import (
    MappedColumn,
    collect_features,
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
        transformer = MappedColumn(
            "col", mapping=mapping, unknown_default=unknown_default
        )
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


@pytest.mark.parametrize(
    "annual_incomes,salary_bands,expected_bands",
    [
        ([10000, 25000, 40000, 60000], [20000, 50000], [0, 1, 1, 2]),
        ([0, 19999, 20000, 50000, 50001], [20000, 50000], [0, 0, 1, 2, 2]),
        ([15000, 35000, 55000], [20000, 40000, 60000], [0, 1, 2]),
        ([70000], [20000, 40000, 60000], [3]),
        ([0], [], [0]),
        ([0], [100], [0]),
    ],
)
def test_assign_salary_bands(monkeypatch, annual_incomes, salary_bands, expected_bands):
    import asec.features as features_mod

    class DummyFields:
        ANNUAL_INCOME = "annual_income"
        SALARY_BAND = "salary_band"

    # Set up dummy CensusASECMetadata.Fields
    monkeypatch.setattr(features_mod.CensusASECMetadata, "Fields", DummyFields)

    df = pd.DataFrame({DummyFields.ANNUAL_INCOME: annual_incomes})
    result = features_mod.assign_salary_bands(df, salary_bands)
    assert DummyFields.SALARY_BAND in result.columns
    assert result[DummyFields.SALARY_BAND].tolist() == expected_bands
