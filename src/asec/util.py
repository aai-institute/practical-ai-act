import pandas as pd
import numpy as np
import logging


log = logging.getLogger(__name__)

def flatten_column(df: pd.DataFrame, column: str, drop_original=True, name_prefix: str = None) -> pd.DataFrame:

    if name_prefix is None:
        name_prefix = column

    values = np.stack(df[column].values)
    if len(values.shape) != 2:
        raise ValueError(f"Column {column} was expected to contain one dimensional vectors, something went wrong")
    dimension = values.shape[1]
    new_columns = [f"{name_prefix}_{i}" for i in range(dimension)]
    log.debug(f"Flattening resulted in {len(new_columns)} new columns")
    flattened_df = pd.DataFrame(values, index=df.index, columns=new_columns)

    df = pd.concat(
        [df.drop(column, axis="columns") if drop_original else df, flattened_df],
        axis=1,
    )
    return df

