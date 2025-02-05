from typing import Protocol, Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class Feature(Protocol):
    def fit(self, X, y=None) -> None: ...

    def transform(self, X): ...


class TakeColumn(BaseEstimator, TransformerMixin):
    def __init__(self, column: str):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[[self.column]]


class MappedColumn(BaseEstimator, TransformerMixin):
    def __init__(
        self, column: str, mapping_dict: dict[str, Any], unknown_default: Any = pd.NA
    ):
        """
        Parameters:
        - column: str, the column to map
        - mapping_dict: dict, the dictionary with mapping values
        - unknown_default:
        """
        self.unknown_default = unknown_default
        self.column = column
        self.mapping_dict = mapping_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[self.column].apply(self._map_value).to_frame()

    def _map_value(self, val):
        if val in set(self.mapping_dict.values()):
            return val

        return self.mapping_dict.get(val, self.unknown_default)


class ColumnDifference(BaseEstimator, TransformerMixin):
    def __init__(self, col1: str, col2: str, resulting_col_name: str):
        self.resulting_col_name = resulting_col_name
        self.col1 = col1
        self.col2 = col2

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return (X[self.col1] - X[self.col2]).to_frame(self.resulting_col_name)
