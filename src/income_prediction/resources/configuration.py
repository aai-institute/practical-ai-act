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

    mlflow_tracking_url: str = "http://localhost:4040"
    mlflow_experiment: str = "Income Prediction"

    random_state: int = 42
