import pandas as pd
from dagster import asset

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.resources.census_asec_downloader import CensusASECDownloader


@asset(io_manager_key="csv_io_manager")
def census_asec_dataset(downloader: CensusASECDownloader) -> pd.DataFrame:
    """Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria.

    This function retrieves the US Census ASEC supplemental dataset from the US Census webserver. It applies filtering
    to align with the characteristics of the UCI Adult dataset (https://archive.ics.uci.edu/dataset/2/adult).

    Filtering criteria:
     - Age must be at least 16 years.
     - Total income must be greater than 100.
     - Hours worked per week non-zero.
     - Final weight must be greater non-zero.

    Parameters
    ----------
    downloader : CensusASECDownloader
        The downloader used to fetch the raw Census ASEC dataset.

    Returns
    -------
    pd.DataFrame
        A filtered dataframe containing the Census ASEC dataset that meets the specified criteria.
    """
    census_data = downloader.download()

    query = (
        f"{CensusASECMetadata.Fields.AGE_YEARS} >= 16 &"
        f"{CensusASECMetadata.Fields.ANNUAL_INCOME} > 100 &"
        f"{CensusASECMetadata.Fields.HOURS_PER_WEEK} > 0 &"
        f"{CensusASECMetadata.Fields.FINAL_WEIGHT} > 0"
    )
    census_data = census_data.query(query)

    return census_data
