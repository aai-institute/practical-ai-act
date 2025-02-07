from typing import Any

import numpy as np
from fastapi import APIRouter

from hr_assistant import dependencies
from hr_assistant.config import MLFLOW_MODEL_URI

router = APIRouter(tags=["model"])


@router.post("/predict")
def predict(
    query: list[float],
    model: dependencies.models.ModelDependency,
    logger: dependencies.logging.PredictionLoggerDependency,
):
    """Run the prediction model on the given input data."""

    input_data = np.array(query)
    proba = model.predict_proba([input_data])
    prediction = float(np.argmax(proba))

    data = {
        "input": input_data.tolist(),
        "output": {
            "class": prediction,
            "probabilities": proba.tolist(),
        },
    }

    logger.log(
        input_data=data["input"],
        output_data=data["output"],
        # FIXME: Model version could contain an alias, must resolve to a definitive version before logging to keep traceability
        metadata={"model_version": MLFLOW_MODEL_URI},
    )

    return data


@router.get("/info")
def info(model: dependencies.models.ModelDependency) -> dict[str, Any]:
    """Return metadata information about the model."""
    return model.metadata.to_dict()


@router.post("/flush-logs")
def flush_logs(logger: dependencies.logging.PredictionLoggerDependency):
    """Flush the prediction log buffer to disk."""
    logger.flush()
    return {"status": "success"}
