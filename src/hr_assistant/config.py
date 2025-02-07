from pathlib import Path

PREDICTION_LOG_PATH = Path("predictions.jsonl")

# FIXME: Parameterize the model name and version
MLFLOW_MODEL_URI = "models:/tracking-quickstart/latest"
