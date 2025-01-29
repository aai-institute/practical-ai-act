from dagster import ConfigurableResource


class Config(ConfigurableResource):
    census_asec_dataset_year: int = 2024
    mlflow_tracking_url: str = "http://localhost:4040"
    mlflow_experiment: str = "Income Prediction"
    data_dir: str = "data"
