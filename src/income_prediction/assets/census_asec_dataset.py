from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from income_prediction.metadata.census_asec_metadata import CensusASECMetadata
from income_prediction.utils.dataset import download_file, extract_file_from_zip


def filter_relevant_census_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the Census ASEC dataset to align with the UCI Adult dataset criteria.

    The filtering criteria (from https://archive.ics.uci.edu/dataset/2/adult) are:
     - Age must be at least 16 years.
     - Total income must be greater than 100.
     - Hours worked per week must be non-zero.
     - Final weight must be greater than zero.

    Parameters
    ----------
    df : pd.DataFrame
        The raw dataset containing Census ASEC records.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only records that meet the criteria.
    """

    query = (
        f"{CensusASECMetadata.Fields.AGE_YEARS} >= 16 & "
        + f"{CensusASECMetadata.Fields.ANNUAL_INCOME} > 100 & "
        + f"{CensusASECMetadata.Fields.HOURS_PER_WEEK} > 0 & "
        + f"{CensusASECMetadata.Fields.FINAL_WEIGHT} > 0"
    )
    return df.query(query)


def download_census_data(year: int) -> pd.DataFrame:
    """Downloads and extracts the Census ASEC supplementary dataset for a given year.

    Parameters
    ----------
    year : int
        Target year for downloading the dataset.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the downloaded dataset.
    """
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march/asecpub{year % 100:02}csv.zip"
    data_file = f"pppub{year % 100:02}.csv"

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        archive_file = temp_path / "data.zip"

        download_file(url, archive_file)
        extract_file_from_zip(archive_file, data_file, temp_path)

        return pd.read_csv(temp_path / data_file)


def download_and_filter_census_data(year: int) -> pd.DataFrame:
    """
    Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria.

    This function retrieves the US Census ASEC supplemental dataset from the Census web server
    and applies filtering to align with the characteristics of the UCI Adult dataset.

    Parameters
    ----------
    year : int
        Target year for downloading the dataset.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing Census ASEC records that meet the specified criteria.
    """
    df = download_census_data(year)
    return filter_relevant_census_data(df)
