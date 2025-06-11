from __future__ import annotations

import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import requests


class CensusASECMetadata:
    """
    Metadata class that provides human-readable mappings for the Census ASEC dataset.

    This includes column names, feature categorizations, and the target variable
    for income prediction.
    """

    class Fields:
        """Mapping of original column names to human-readable names for Census ASEC data."""

        # Demographics
        AGE_YEARS = "A_AGE"
        SEX = "A_SEX"
        EDUCATION_LEVEL = "A_HGA"
        ENROLLMENT_STATUS = "A_ENRLW"
        ENROLLMENT_TYPE = "A_FTPT"
        SCHOOL_ENROLLMENT = "A_HSCOL"
        MARITAL_STATUS = "A_MARITL"
        HOUSEHOLD_RELATIONSHIP = "P_STAT"
        HAS_CERTIFICATION = "PECERT1"
        HISPANIC_ORIGIN = "PEHSPNON"
        HISPANIC_ETHNICITY = "PRDTHSP"
        ASIAN_ETHNICITY = "PRDASIAN"
        RACE = "PRDTRACE"
        COUNTRY_OF_BIRTH = "PENATVTY"
        CITIZENSHIP_STATUS = "PRCITSHP"
        DISABILITY_STATUS = "PRDISFLG"

        # Employment & Work
        EMPLOYMENT_STATUS = "A_LFSR"
        EMPLOYMENT_CLASS = "A_CLSWKR"
        FULL_TIME_LABOR_FORCE = "A_FTLF"
        UNION_MEMBERSHIP = "A_UNMEM"
        UNEMPLOYMENT_TYPE = "A_UNTYPE"
        UNEMPLOYMENT_REASON = "PRUNTYPE"
        UNEMPLOYMENT_DURATION = "A_WKSLK"
        WORK_HOURS_CATEGORY = "A_WKSTAT"
        WORK_WEEKS = "WKSWORK"
        USUAL_HOURS_PER_WEEK = "A_USLHRS"
        HOURS_PER_WEEK = "HRSWK"
        EDITED_WORK_HOURS = "A_HRS1"
        EMPLOYEE_COUNT = "NOEMP"
        INDUSTRY = "INDUSTRY"
        LONGEST_JOB_CLASS = "CLWK"
        MAJOR_INDUSTRY = "A_MJIND"
        MAJOR_OCCUPATION = "A_MJOCC"
        MAJOR_LABOR_FORCE = "PEMLR"

        # Income & Earnings
        WEEKLY_EARNINGS = "A_GRSWK"
        HOURLY_WAGE = "A_HRSPAY"
        LONGEST_JOB_INCOME_SOURCE = "ERN_SRCE"
        LONGEST_JOB_EARNINGS = "ERN_VAL"
        ANNUAL_EARNINGS = "PEARNVAL"
        SELF_EMPLOYMENT_INCOME = "SEMP_VAL"
        SECOND_JOB_INCOME = "WAGEOTR"
        ANNUAL_INCOME = "PTOTVAL"
        INCOME_IN_RANGE = "INCOME_IN_RANGE"
        ADJUSTED_GROSS_INCOME = "AGI"

        # Health & Insurance
        HAS_HEALTH_INSURANCE = "COV"
        SELF_REPORTED_HEALTH = "HEA"

        # Weights
        FINAL_WEIGHT = "A_FNLWGT"

    # Target variable
    TARGET = Fields.INCOME_IN_RANGE

    # Feature categories
    CATEGORICAL_FEATURES = [
        Fields.SEX,
        Fields.ENROLLMENT_STATUS,
        Fields.ENROLLMENT_TYPE,
        Fields.SCHOOL_ENROLLMENT,
        Fields.MARITAL_STATUS,
        Fields.HOUSEHOLD_RELATIONSHIP,
        Fields.HAS_CERTIFICATION,
        Fields.HISPANIC_ORIGIN,
        Fields.HISPANIC_ETHNICITY,
        Fields.ASIAN_ETHNICITY,
        Fields.RACE,
        Fields.COUNTRY_OF_BIRTH,
        Fields.CITIZENSHIP_STATUS,
        Fields.DISABILITY_STATUS,
        Fields.EMPLOYMENT_STATUS,
        Fields.EMPLOYMENT_CLASS,
        Fields.FULL_TIME_LABOR_FORCE,
        Fields.UNION_MEMBERSHIP,
        Fields.UNEMPLOYMENT_TYPE,
        Fields.UNEMPLOYMENT_REASON,
        Fields.WORK_HOURS_CATEGORY,
        Fields.INDUSTRY,
        Fields.LONGEST_JOB_CLASS,
        Fields.MAJOR_INDUSTRY,
        Fields.MAJOR_OCCUPATION,
        Fields.MAJOR_LABOR_FORCE,
        Fields.LONGEST_JOB_INCOME_SOURCE,
        Fields.HAS_HEALTH_INSURANCE,
        Fields.SELF_REPORTED_HEALTH,
    ]

    NUMERIC_FEATURES = [
        Fields.AGE_YEARS,
        Fields.UNEMPLOYMENT_DURATION,
        Fields.WORK_WEEKS,
        Fields.USUAL_HOURS_PER_WEEK,
        Fields.HOURS_PER_WEEK,
        Fields.EDITED_WORK_HOURS,
        Fields.EMPLOYEE_COUNT,
        Fields.WEEKLY_EARNINGS,
        Fields.HOURLY_WAGE,
        Fields.LONGEST_JOB_EARNINGS,
        Fields.SECOND_JOB_INCOME,
        Fields.ADJUSTED_GROSS_INCOME,
        Fields.FINAL_WEIGHT,
    ]

    ORDINAL_FEATURES = [
        Fields.EDUCATION_LEVEL,
    ]

    TO_EXCLUDE = [Fields.WEEKLY_EARNINGS,
          Fields.HOURLY_WAGE,
          Fields.LONGEST_JOB_EARNINGS,
          Fields.SECOND_JOB_INCOME,
          Fields.ADJUSTED_GROSS_INCOME,
          Fields.ANNUAL_INCOME,
          Fields.FINAL_WEIGHT,
          Fields.ANNUAL_EARNINGS,
          Fields.SELF_EMPLOYMENT_INCOME,
          Fields.SECOND_JOB_INCOME,
        ]



def download_file(url: str, destination: Path) -> None:
    """Downloads a file from the given url and saves it to the specified destination.

    Parameters
    ----------
    url : str
        URL to download the file from.
    destination : Path
        The local path where the downloaded file should be saved.

    Raises
    ------
    ValueError
        If the file download fails.
    """
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    with open(destination, "wb") as file:
        file.write(response.content)


def extract_file_from_zip(zip_path: Path, expected_file: str, extract_to: Path) -> None:
    """Extracts a specific file from a ZIP archive.

    Parameters
    ----------
    zip_path : Path
        Path to the ZIP archive.
    expected_file : str
        Name of the file to extract.
    extract_to : str
        Directory where the extracted file should be saved.

    Raises
    ------
    ValueError
        If the ZIP archive is invalid or does not contain the expected file.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            if expected_file not in zip_ref.namelist():
                raise ValueError(f"File '{expected_file}' not found in ZIP archive.")

            zip_ref.extract(expected_file, extract_to)
    except zipfile.BadZipFile as e:
        raise ValueError(f"Invalid ZIP archive: {e}") from e


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


def download_census_data(year: int, use_archive: bool = False) -> pd.DataFrame:
    """Downloads and extracts the Census ASEC supplementary dataset for a given year.

    Parameters
    ----------
    year : int
        Target year for downloading the dataset.
    use_archive : bool, optional
        If True, use the Internet Archive to download the dataset. Default is False.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the downloaded dataset.
    """

    archive_base_url = "https://web.archive.org/web/20250302225052/"
    base_url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march"

    if use_archive:
        base_url = archive_base_url + base_url

    url = f"{base_url}/asecpub{year % 100:02}csv.zip"
    data_file = f"pppub{year % 100:02}.csv"

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        archive_file = temp_path / "data.zip"

        download_file(url, archive_file)
        extract_file_from_zip(archive_file, data_file, temp_path)

        return pd.read_csv(temp_path / data_file)


def download_and_filter_census_data(
    year: int, use_archive: bool = False
) -> pd.DataFrame:
    """
    Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria.

    This function retrieves the US Census ASEC supplemental dataset from the Census web server
    and applies filtering to align with the characteristics of the UCI Adult dataset.

    Parameters
    ----------
    year : int
        Target year for downloading the dataset.
    use_archive : bool, optional
        If True, use the Internet Archive to download the dataset. Default is False.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing Census ASEC records that meet the specified criteria.
    """
    df = download_census_data(year, use_archive=use_archive)
    return filter_relevant_census_data(df)
