import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from hr_assistant.dependencies.models import ModelDependency
from hr_assistant.dependencies.logging import PredictionLoggerDependency
from hr_assistant.config import MODEL_URI


def to_kebab(field: str) -> str:
    return field.replace("_", "-")


class ModelInput(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
    )

    age: int
    workclass: str
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: float
    native_country: str


router = APIRouter(tags=["model"])


@router.post("/predict")
def predict(
    model_input: ModelInput | list[ModelInput],
    model: ModelDependency,
    logger: PredictionLoggerDependency,
):
    if not isinstance(model_input, list):
        model_input = [model_input]
    input_data = pd.DataFrame.from_records(
        m.model_dump(by_alias=True) for m in model_input
    )
    prediction = model.predict(input_data)
    proba = model.predict_proba(input_data)

    data = {
        "input": input_data.to_dict(orient="records"),
        "output": {
            "class": prediction.tolist(),
            "probabilities": proba.tolist(),
        },
    }

    logger.log(
        input_data=data["input"],
        output_data=data["output"],
        # FIXME: Model version could contain an alias, must resolve to a definitive version before logging to keep traceability
        metadata={"model_version": MODEL_URI},
    )

    return data
