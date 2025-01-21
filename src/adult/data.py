from __future__ import annotations

from tkinter import W
import urllib
import urllib.request
import zipfile
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from sensai import InputOutputData
from sensai.util.cache import pickle_cached
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
            loading_func = pickle_cached(data_path)(loading_func)

        self._data = loading_func(id=2)

    def load_data_frame(self) -> pd.DataFrame:
        """
        Load the data as a pandas DataFrame.
        """
        df = self._data.data.original
        df.loc[:, self.TARGET] = df[self.TARGET].map(lambda x: x.rstrip("."))
        return df

    def load_input_output_data(self) -> InputOutputData:
        """
        Load the data as an `InputOutputData` object used in the
        [`sensai`](https://github.com/opcode81/sensAI) package.
        """
        all_df = self.load_data_frame()
        return InputOutputData(
            all_df.drop(columns=[self.TARGET]), all_df[[self.TARGET]]
        )


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

    def load_input_output_data(self) -> InputOutputData:
        df = self.load_data_frame()
        return InputOutputData(
            inputs=df[
                [
                    col
                    for col in self.COLS_CATEGORICAL
                    + self.COLS_NUMERIC
                    + self.COLS_ORDINAL
                ]
            ],
            outputs=df[[self.TARGET]],
        )
