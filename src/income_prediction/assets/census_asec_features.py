import numpy as np
import pandas as pd
from dagster import asset

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.resources.configuration import Config


@asset(io_manager_key="csv_io_manager")
def census_asec_features(config: Config, census_asec_dataset: pd.DataFrame) -> pd.DataFrame:
    """Pre-processes the Census ASEC dataset for income prediction.

    - Assigns each individual a salary band based on their total income.
    - Selects relevant categorical, numerical, and ordinal features, and the target value.

    Parameters
    ----------
    config : Config
        The pipeline configuration, containing the salary band thresholds.
    census_asec_dataset : pd.DataFrame
        The raw Census ASEC supplementary dataset.

    Returns
    -------
    pd.DataFrame
        The preprocessed dataframe containing selected features and salary band classifications.
    """

    # Assign salary band classification
    census_asec_dataset[CensusASECMetadata.TARGET] = np.searchsorted(
        config.salary_bands,
        census_asec_dataset[CensusASECMetadata.Fields.ANNUAL_INCOME],
        side="right",
    )

    # Select relevant features
    selected_features = (
        CensusASECMetadata.CATEGORICAL_FEATURES
        + CensusASECMetadata.NUMERIC_FEATURES
        + CensusASECMetadata.ORDINAL_FEATURES
        + [CensusASECMetadata.TARGET]
    )
    return census_asec_dataset[selected_features]
