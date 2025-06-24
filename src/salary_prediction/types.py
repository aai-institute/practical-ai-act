from dataclasses import dataclass


@dataclass
class ModelVersion:
    """Represents a model version in the MLflow model registry."""

    version: str
    name: str
    uri: str
