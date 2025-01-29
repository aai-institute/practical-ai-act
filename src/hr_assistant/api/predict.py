import random
import string
from datetime import datetime

from fastapi import APIRouter

from hr_assistant import dependencies

router = APIRouter(tags=["model"])

# FIXME: Replace hardcoded model info with actual model info
_metadata = {
    "model_version": datetime.now().strftime("%Y%m%d")
    + "-"
    + "".join(random.sample(string.hexdigits, 6)),
}


@router.post("/predict")
def predict(
    query: str,
    logger: dependencies.logging.PredictionLoggerDependency,
):
    """Run the prediction model on the given input data."""
    data = {
        "input": query,
        "output": query.upper(),
    }

    logger.log(
        data["input"],
        data["output"],
        {"model_metadata": _metadata},
    )

    return data


@router.get("/info")
def info():
    """Return metadata information about the model."""
    return _metadata
