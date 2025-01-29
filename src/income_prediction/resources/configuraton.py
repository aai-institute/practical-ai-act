from dagster import ConfigurableResource


class Config(ConfigurableResource):
    census_asec_dataset_year: int = 2024
