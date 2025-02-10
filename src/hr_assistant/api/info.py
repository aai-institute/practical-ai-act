from fastapi import APIRouter
from hr_assistant.dependencies.models import ModelDependency

router = APIRouter(tags=["model"])


@router.get("/info")
def model_info(model: ModelDependency):
    return str(model)
