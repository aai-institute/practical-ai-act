from dagster import ConfigurableResource


class Config(ConfigurableResource):
    """Pipeline configuration."""

    census_asec_dataset_year: int = 2024

    salary_bands: list[int] = [
        35000,  # Entry level
        55000,  # Lower mid-range
        85000,  # Mid-range
        120000,  # Upper mid-range
    ]  # > 120000 High

    data_dir: str = "data"

    mlflow_tracking_url: str = "http://localhost:50000"
    mlflow_experiment: str = "Income Prediction"

    lakefs_host: str = "http://localhost:8000"
    lakefs_access_key_id: str = "AKIAIOSFOLKFSSAMPLES"
    lakefs_secret_access_key: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    lakefs_verify_ssl: bool = False

    random_state: int = 42
