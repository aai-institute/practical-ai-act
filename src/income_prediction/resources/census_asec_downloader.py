import urllib.request
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from dagster import ConfigurableResource

from income_prediction.census_asec_data_description import CensusASECDataDescription

_LB, _UB = 1994, 2024


class CensusASECDownloader(ConfigurableResource):
    """
    Download the census ASEC data for a given year.

    Attributes
    ----------
    year: int
        The year to download the data for.
    """
    year: int

    def download(self) -> pd.DataFrame:
        if not _LB <= self.year <= _UB:
            # TODO(nicholasjng): Refine this check
            raise ValueError(f"only years between {_LB} and {_UB} are available")

        shortyear = str(self.year)[-2:]
        url = f"https://www2.census.gov/programs-surveys/cps/datasets/{shortyear}/march/asecpub{shortyear}csv.zip"
        data_file = f"pppub{shortyear}.csv"

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_file = temp_path / "data.zip"
            urllib.request.urlretrieve(url, archive_file)
            zipfile.ZipFile(archive_file).extract(data_file, temp_dir)

            df = pd.read_csv(temp_path / data_file)

            # Apply subsetting from original UCI Adult Income dataset
            df = df[
                (df[CensusASECDataDescription.Column.AGE] >= 16)
                & (df[CensusASECDataDescription.Column.TOTAL_INCOME] > 100)
                & (df[CensusASECDataDescription.Column.HOURS_PER_WEEK] > 0)
                & (df[CensusASECDataDescription.Column.FNLWGT] > 0)
            ]

            return df
