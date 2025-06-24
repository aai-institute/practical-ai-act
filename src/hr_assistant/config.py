import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    # Open Inference Protocol v2 REST server
    inference_base_url: str = "http://model:8080"

    model_name: str = "salary-predictor"
    model_version: str = "latest"

    db_user: str = "postgres_user"
    db_password: str = "postgres_password"
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "hr_assistant"


settings = Settings()
