import os
from pathlib import Path

_config_file_folder = os.path.dirname(os.path.abspath(__file__))
DATA_SUBFOLDER = Path(_config_file_folder).parent / "data"
RESULT_SUBFOLDER = Path(_config_file_folder).parent / "results"
MLFLOW_SUBFOLDER = Path(_config_file_folder).parent / "mlruns"

FILE_NAME = DATA_SUBFOLDER / "german_credit_data"
FILE_NAME_ADULT = DATA_SUBFOLDER / "adult_data"
FILE_NAME_ASEC = DATA_SUBFOLDER / "asec_data"
