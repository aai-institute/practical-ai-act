from __future__ import annotations

import urllib
import urllib.request
import zipfile
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
from folktables import ACSDataSource, BasicProblem, adult_filter

from ucimlrepo import fetch_ucirepo


class AdultData:
    """
    Data provider for the [`Census Income` dataset](https://archive.ics.uci.edu/dataset/2/adult) from UCI repository.
    Also known as `Adult` dataset. The provider loads the data using the [`ucimlrepo`](https://github.com/uci-ml-repo/ucimlrepo) package
    and optionally caches the data using the `pickle` module.

    Args:
        data_path: Optional directory to cache the downloaded result.
            If not provided, the data will be downloaded from the UCI repository directly.
    """

    class Column(str, Enum):
        """
        Enum representing the column names in the original data
        """

        AGE = "age"
        WORK_CLASS = "workclass"
        FNLWGT = "fnlwgt"
        EDUCATION = "education"
        EDUCATION_NUM = "education-num"
        MARITAL_STATUS = "marital-status"
        OCCUPATION = "occupation"
        RELATIONSHIP = "relationship"
        SEX = "sex"
        RACE = "race"
        CAPITAL_GAIN = "capital-gain"
        CAPITAL_LOSS = "capital-loss"
        HOURS_PER_WEEK = "hours-per-week"
        NATIVE_COUNTRY = "native-country"
        INCOME = "income"

    TARGET = Column.INCOME
    CLASS_POSITIVE = ">50K"
    COLS_CATEGORICAL = (
        Column.EDUCATION,
        Column.MARITAL_STATUS,
        Column.NATIVE_COUNTRY,
        Column.RELATIONSHIP,
        Column.SEX,
        Column.RACE,
        Column.WORK_CLASS,
        Column.OCCUPATION,
    )
    COLS_NUMERIC = (
        Column.HOURS_PER_WEEK,
        Column.EDUCATION_NUM,
        Column.AGE,
        Column.CAPITAL_GAIN,
        Column.CAPITAL_LOSS,
    )

    def __init__(self, data_path: str | Path | None = None):
        self._data_path = data_path

        loading_func = fetch_ucirepo

        if data_path is not None:
            from sensai.util.cache import pickle_cached

            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(id=2)

    def load_data_frame(self) -> pd.DataFrame:
        """
        Load the data as a pandas DataFrame.
        """
        df = self._data.data.original
        df.loc[:, self.TARGET] = df[self.TARGET].map(lambda x: x.rstrip("."))
        return df

    def load_input_output_data(self) -> tuple[pd.DataFrame, pd.Series]:
        """
        Load the data as an `InputOutputData` object used in the
        """
        all_df = self.load_data_frame()
        return all_df.drop(columns=[self.TARGET]), all_df[self.TARGET]


def _fetch_asec_data(
    data_path: str | Path,
    year: int = 2024,
) -> pd.DataFrame:
    """Return the US Census CPS ASEC supplemental dataset for a given year as a DataFrame."""
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/march/asecpub{year % 2000}csv.zip"
    data_file = f"pppub{year % 2000}.csv"

    with TemporaryDirectory() as temp_dir:
        archive_file = temp_dir + "/data.zip"
        urllib.request.urlretrieve(url, archive_file)
        zipfile.ZipFile(archive_file).extract(data_file, data_path)
        df = pd.read_csv(data_path / data_file)
        return df


class AdultASECData:
    """
    Data provider for the US Census CPS ASEC supplemental dataset.

    2024 dataset data dictionary: https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asec2024_ddl_pub_full.pdf

    The provider loads the data from the US Census web server and optionally caches the data using the `pickle` module.

    Args:
        data_path: Optional directory to cache the downloaded result.
            If not provided, the data will be downloaded from the US Census web server.
    """

    class Column(str, Enum):
        """
        Enum representing the column names in the original data
        """

        AGE = "A_AGE"
        ENROL_STATUS = "A_ENRLW"
        ENROL_FULL_TIME_PART_TIME = "A_FTPT"
        EDUCATION = "A_HGA"
        ENROL_SCHOOL = "A_HSCOL"
        MARITAL_STATUS = "A_MARITL"
        SEX = "A_SEX"
        PERSON_STATUS = "P_STAT"
        PROFESSIONAL_CERTIFICATION = "PECERT1"
        SPANISH_HISPANIC_LATINO = "PEHSPNON"
        BIRTH_COUNTRY = "PENATVTY"
        CITIZENSHIP_GROUP = "PRCITSHP"
        ASIAN_SUBGROUP = "PRDASIAN"
        DISABILITY_CONDITIONS = "PRDISFLG"
        HISPANIC_SUBGROUP = "PRDTHSP"
        RACE = "PRDTRACE"

        # Allocation flags
        ALLOCATED_AGE = "AXAGE"
        ALLOCATED_ENROL_STATUS = "AXENRLW"
        ALLOCATED_ENROL_FULL_TIME_PART_TIME = "AXFTPT"
        ALLOCATED_EDUCATION = "AXHGA"
        ALLOCATED_ENROL_SCHOOL = "AXHSCOL"
        ALLOCATED_MARITAL_STATUS = "PXMARITL"
        ALLOCATED_SEX = "AXSEX"
        ALLOCATED_PROFESSIONAL_CERTIFICATION = "PXCERT1"
        ALLOCATED_SPANISH_HISPANIC_LATINO = "PXHSPNON"
        ALLOCATED_BIRTH_COUNTRY = "PXNATVTY"
        ALLOCATED_CITIZENSHIP_GROUP = "PRCITFLG"
        ALLOCATED_RACE = "PXRACE1"
        ALLOCATED_EARNINGS_GROSS_PER_WEEK = "PRWERNAL"
        ALLOCATED_CLASS_OF_WORKER = "AXCLSWKR"
        ALLOCATED_HOURS_PER_WEEK_EDITED = "AXHRS"
        ALLOCATED_LABOR_FORCE_STATUS = "AXLFSR"
        ALLOCATED_UNION_MEMBERSHIP = "AXUNMEM"
        ALLOCATED_HOURS_PER_WEEK = "I_HRSWK"
        ALLOCATED_INDUSTRY = "I_INDUS"
        ALLOCATED_LONGEST_JOB_CLASS = "I_LJCW"
        ALLOCATED_NUMBER_OF_EMPLOYEES = "I_NOEMP"
        ALLOCATED_WEEKS_WORKED = "I_WKSWK"
        ALLOCATED_LONGEST_JOB_EARNINGS_SOURCE = "I_ERNSRC"
        ALLOCATED_LONGEST_JOB_EARNINGS = "I_ERNVAL"
        ALLOCATED_TOTAL_EARNINGS = "I_PEARN"
        ALLOCATED_HEALTH_STATUS = "I_HEA"

        # FIXME: Add topcode flags

        # Edited labor force items
        HOURS_PER_WEEK_EDITED = "A_HRS1"
        MAJOR_INDUSTRY = "A_MJIND"
        MAJOR_OCCUPATION = "A_MJOCC"
        UNEMPLOYMENT_REASON = "PRUNTYPE"

        # Edited earnings items
        EARNINGS_GROSS_PER_WEEK = "A_GRSWK"
        HOURLY_PAY = "A_HRSPAY"

        # Labor force person recodes
        WORKER_CLASS = "A_CLSWKR"
        FULL_TIME_LABOR_FORCE = "A_FTLF"
        LABOR_FORCE_STATUS = "A_LFSR"
        UNION_MEMBERSHIP = "A_UNMEM"
        UNEMPLOYMENT_TYPE = "A_UNTYPE"
        USUAL_HOURS_PER_WEEK = "A_USLHRS"
        UNEMPLOYMENT_DURATION = "A_WKSLK"
        FULL_TIME_PART_TIME_STATUS = "A_WKSTAT"
        MAJOR_LABOR_FORCE = "PEMLR"

        # Work experience
        LONGEST_JOB_CLASS = "CLWK"
        HOURS_PER_WEEK = "HRSWK"
        INDUSTRY = "INDUSTRY"
        NUMBER_OF_EMPLOYEES = "NOEMP"
        WEEKS_WORKED = "WKSWORK"

        # Income
        LONGEST_JOB_EARNINGS_SOURCE = "ERN_SRCE"
        LONGEST_JOB_EARNINGS = "ERN_VAL"
        TOTAL_EARNINGS = "PEARNVAL"
        SELF_EMPLOYED_EARNINGS = "SEMP_VAL"
        OTHER_EMPLOYERS_WAGE = "WAGEOTR"
        TOTAL_INCOME = "PTOTVAL"

        # Tax model items
        ADJUSTED_GROSS_INCOME = "AGI"

        # Health Insurance
        HEALTH_INSURANCE_COVERAGE = "COV"

        # Health status
        HEALTH_STATUS = "HEA"

        FNLWGT = "A_FNLWGT"

    TARGET = Column.TOTAL_INCOME

    COLS_CATEGORICAL = (
        Column.ENROL_STATUS,
        Column.ENROL_FULL_TIME_PART_TIME,
        Column.ENROL_SCHOOL,
        Column.MARITAL_STATUS,
        Column.SEX,
        Column.PERSON_STATUS,
        Column.PROFESSIONAL_CERTIFICATION,
        Column.SPANISH_HISPANIC_LATINO,
        Column.BIRTH_COUNTRY,
        Column.CITIZENSHIP_GROUP,
        Column.ASIAN_SUBGROUP,
        Column.DISABILITY_CONDITIONS,
        Column.HISPANIC_SUBGROUP,
        Column.RACE,
        Column.MAJOR_INDUSTRY,
        Column.MAJOR_OCCUPATION,
        Column.UNEMPLOYMENT_REASON,
        Column.WORKER_CLASS,
        Column.FULL_TIME_LABOR_FORCE,
        Column.LABOR_FORCE_STATUS,
        Column.UNION_MEMBERSHIP,
        Column.UNEMPLOYMENT_TYPE,
        Column.FULL_TIME_PART_TIME_STATUS,
        Column.MAJOR_LABOR_FORCE,
        Column.LONGEST_JOB_CLASS,
        Column.INDUSTRY,
        Column.LONGEST_JOB_EARNINGS_SOURCE,
        Column.OTHER_EMPLOYERS_WAGE,
        Column.HEALTH_INSURANCE_COVERAGE,
        Column.HEALTH_STATUS,
    )
    COLS_NUMERIC = (
        Column.AGE,
        Column.HOURS_PER_WEEK_EDITED,
        Column.EARNINGS_GROSS_PER_WEEK,
        Column.HOURLY_PAY,
        Column.USUAL_HOURS_PER_WEEK,
        Column.UNEMPLOYMENT_DURATION,
        Column.HOURS_PER_WEEK,
        Column.WEEKS_WORKED,
        Column.LONGEST_JOB_EARNINGS,
        Column.TOTAL_EARNINGS,
        Column.SELF_EMPLOYED_EARNINGS,
        Column.ADJUSTED_GROSS_INCOME,
        Column.FNLWGT,
    )
    COLS_ORDINAL = (
        Column.EDUCATION,
        Column.NUMBER_OF_EMPLOYEES,
    )

    def __init__(self, data_path: str | Path | None = None, year: int = 2024):
        self._data_path = data_path

        loading_func = _fetch_asec_data
        if data_path is not None:
            from sensai.util.cache import pickle_cached

            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(year=year, data_path=data_path)

    def load_data_frame(self) -> pd.DataFrame:
        df = self._data

        # Apply subsetting from original UCI Adult Income dataset
        df = df[
            (df[self.Column.AGE] >= 16)
            & (df[self.Column.TOTAL_INCOME] > 100)
            & (df[self.Column.HOURS_PER_WEEK] > 0)
            & (df[self.Column.FNLWGT] > 0)
        ]
        return df

    def load_input_output_data(self) -> tuple[pd.DataFrame, pd.Series]:
        df = self.load_data_frame()
        inputs: pd.DataFrame = df[
            list(self.COLS_CATEGORICAL + self.COLS_NUMERIC + self.COLS_ORDINAL)
        ]
        outputs: pd.Series = df[[self.TARGET]]
        return inputs, outputs


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
        GENDER = "A_SEX"
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
        SALARY_BAND = "SALARY_BAND"
        ADJUSTED_GROSS_INCOME = "AGI"

        # Health & Insurance
        HAS_HEALTH_INSURANCE = "COV"
        SELF_REPORTED_HEALTH = "HEA"

        # Weights
        FINAL_WEIGHT = "A_FNLWGT"

    # Target variable
    TARGET = Fields.SALARY_BAND

    # Feature categories
    CATEGORICAL_FEATURES = [
        Fields.GENDER,
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
    try:
        urllib.request.urlretrieve(url, destination)
    except urllib.error.URLError as e:
        raise ValueError(f"Failed to download data from {url}: {e}") from e


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

def download_pums_data(year: int, base_dir: str | PathLike = "data"):
  """
  This function uses the `folktables` library to download
  the Public Use Microdata Sample (PUMS) data from the US Census Bureau.

  Args:
    year: The year for which the PUMS data is to be downloaded.
    base_dir: The base directory where the data will be stored.

  Returns:
    pd.DataFrame: The downloaded PUMS data as a pandas DataFrame.

  """
  data_source = ACSDataSource(survey_year=year,
                              horizon='1-Year',
                              survey='person',
                              root_dir=base_dir,
                              use_archive=True)
  return data_source.get_data(download=True)

def filter_pums_data(df: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:


  spec = BasicProblem(
    features=features,
    target=PUMSMetaData.Fields.ANNUAL_INCOME,
    preprocess=adult_filter,
    #postprocess=lambda x: np.nan_to_num(x, -1),
  )

  feature_df, target_df, _ = spec.df_to_pandas(df)
  return feature_df, target_df

def binning_targets(target_df: pd.DataFrame, target_bins: list[int]) -> pd.DataFrame:
  values = np.searchsorted(
    target_bins, target_df[PUMSMetaData.Fields.ANNUAL_INCOME], side="right"
  )
  return pd.DataFrame(data=values, columns=[PUMSMetaData.SALARY_BAND])

def transform_to_categorical(feature_df: pd.DataFrame) -> pd.DataFrame:
  cat_cols = set(PUMSMetaData.CATEGORICAL_FEATURES).intersection(
    set(feature_df.columns))

  for col in cat_cols:
    feature_df[col] = feature_df[col].astype("category")

  return feature_df.infer_objects()


class PUMSMetaData:

  class Fields:
    """
    Mapping of original column names to human-readable names for PUMS data.
    """

    # Demographics
    AGE_YEARS = "AGEP"
    GENDER = "SEX"
    MARITAL_STATUS = "MAR"
    HOUSEHOLD_RELATIONSHIP = "RELSHIPP"
    HISPANIC_ETHNICITY = "HISP"
    ASIAN_ETHNICITY = "RACASN"
    RACE = "RAC1P"
    COUNTRY_OF_BIRTH = "POBP"
    CITIZENSHIP_STATUS = "CIT"
    DISABILITY_STATUS = "DIS"
    STATE = "STATE"

    # Education
    EDUCATION_LEVEL = "SCHL"
    ENROLLMENT_STATUS = "SCH"
    ENROLLMENT_TYPE = "SCHG"
    FIELD_OF_DEGREE = "FOD1P"
    HAS_SCIENCE_DEGREE = "SCIENGP"

    # Employment & Work
    EMPLOYMENT_STATUS = "ESR"
    EMPLOYMENT_CLASS = "COW"
    INDUSTRY = "INDP"
    PLACE_OF_WORK = "POWSP"
    HOURS_PER_WEEK = "WKHP"
    WORK_WEEKS = "WKWN"
    LAST_WORKED = "WKL"
    MAJOR_INDUSTRY = "NAICSP"
    MAJOR_OCCUPATION = "OCCP"

    # Income & Earnings
    ANNUAL_INCOME = "PINCP"

    # Health & Insurance
    HAS_HEALTH_INSURANCE = "HICOV"


  # Target variable
  ORIGINAL_TARGET = Fields.ANNUAL_INCOME
  SALARY_BAND = "SALARY_BAND"
  TARGET = SALARY_BAND



  # Feature categories
  CATEGORICAL_FEATURES = [
    Fields.GENDER,
    Fields.ENROLLMENT_STATUS,
    Fields.ENROLLMENT_TYPE,
    Fields.MARITAL_STATUS,
    Fields.HOUSEHOLD_RELATIONSHIP,
    Fields.HISPANIC_ETHNICITY,
    Fields.ASIAN_ETHNICITY,
    Fields.RACE,
    Fields.COUNTRY_OF_BIRTH,
    Fields.CITIZENSHIP_STATUS,
    Fields.DISABILITY_STATUS,
    Fields.STATE,
    Fields.FIELD_OF_DEGREE,
    Fields.HAS_SCIENCE_DEGREE,
    Fields.EMPLOYMENT_CLASS,
    Fields.INDUSTRY,
    Fields.PLACE_OF_WORK,
    Fields.LAST_WORKED,
    Fields.MAJOR_INDUSTRY,
    Fields.MAJOR_OCCUPATION,
    Fields.HAS_HEALTH_INSURANCE
  ]

  NUMERIC_FEATURES = [
    Fields.WORK_WEEKS,
    Fields.HOURS_PER_WEEK,
    Fields.AGE_YEARS,
  ]

  ORDINAL_FEATURES = [
    Fields.EDUCATION_LEVEL
  ]

  FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES + ORDINAL_FEATURES
  REASSEMBLED_ADULT_FEATURES = [
    Fields.AGE_YEARS,
    Fields.EMPLOYMENT_CLASS,
    Fields.EDUCATION_LEVEL,
    Fields.MARITAL_STATUS,
    Fields.MAJOR_OCCUPATION,
    Fields.COUNTRY_OF_BIRTH,
    Fields.HOUSEHOLD_RELATIONSHIP,
    Fields.HOURS_PER_WEEK,
    Fields.GENDER,
    Fields.RACE,
    Fields.FIELD_OF_DEGREE,
    Fields.HAS_SCIENCE_DEGREE
  ]
