import pytest
import pandas as pd
import numpy as np

from asec.util import flatten_column


@pytest.mark.parametrize("df, column, drop_original, name_prefix, expected", [
    (pd.DataFrame({'A': [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]}), 'A', True, None, pd.DataFrame({'A_0': [1, 3, 5], 'A_1': [2, 4, 6]})),
    (pd.DataFrame({'A': [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]}), 'A', True, 'B', pd.DataFrame({'B_0': [1, 3, 5], 'B_1': [2, 4, 6]})),
    (pd.DataFrame({'A': [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]}), 'A', False, None, pd.DataFrame({'A': [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])], 'A_0': [1, 3, 5], 'A_1': [2, 4, 6]})),
])
def test_flatten_column(df, column, drop_original, name_prefix, expected):
    result = flatten_column(df, column, drop_original, name_prefix)
    pd.testing.assert_frame_equal(result, expected)

def test_flatten_column_invalid_shape():
    df = pd.DataFrame({'A': [1, 2, 3]})
    with pytest.raises(ValueError, match="Column A was expected to contain one dimensional vectors, something went wrong"):
        flatten_column(df, 'A')