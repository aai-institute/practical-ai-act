import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from hr_assistant.api.exceptions import InferenceError
from hr_assistant.dependencies.models import InferenceClientDependency


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
    hours_per_week: int
    native_country: str
    fnlwgt: int


router = APIRouter(tags=["model"])


@router.post("/predict")
async def predict(
    model_input: ModelInput | list[ModelInput],
    inference_client: InferenceClientDependency,
):
    if not isinstance(model_input, list):
        model_input = [model_input]
    input_data = pd.DataFrame.from_records(
        m.model_dump(by_alias=True) for m in model_input
    )

    request = inference_client.build_request(input_data)
    try:
        return await inference_client.predict(request)
    except InferenceError as e:
        raise HTTPException(status_code=500, detail=e.response.error) from e
