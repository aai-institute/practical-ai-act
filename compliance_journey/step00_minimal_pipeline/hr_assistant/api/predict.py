import pandas as pd
from fastapi import APIRouter
from hr_assistant.dependencies.models import ModelDependency
from pydantic import BaseModel, ConfigDict, alias_generators, AliasGenerator


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
def predict(model_input: ModelInput | list[ModelInput], model: ModelDependency):
    if not isinstance(model_input, list):
        model_input = [model_input]
    data = pd.DataFrame.from_records(m.model_dump(by_alias=True) for m in model_input)
    return model.predict(data).tolist()
