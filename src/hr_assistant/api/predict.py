from typing import Any

import numpy as np
from fastapi import APIRouter

from hr_assistant import dependencies

router = APIRouter(tags=["model"])


@router.post("/predict")
def predict(
    query: list[float],
    model: dependencies.models.ModelDependency,
    logger: dependencies.logging.PredictionLoggerDependency,
):
    """Run the prediction model on the given input data."""

    input_data = np.array([query])
    output = model.predict(input_data)

    data = {
        "input": input_data.tolist(),
        "output": output.tolist(),
    }

    logger.log(
        data["input"],
        data["output"],
        metadata={"model_uuid": model.metadata.model_uuid},
    )

    return data


@router.get("/info")
def info(model: dependencies.models.ModelDependency) -> dict[str, Any]:
    """Return metadata information about the model."""
    return model.metadata.to_dict()


@router.post("/flush-logs")
def flush_logs(logger: dependencies.logging.PredictionLoggerDependency):
    """Flush the prediction log buffer to disk."""
    logger._buffer.flush()
    return {"status": "success"}
