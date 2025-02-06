from fastapi import APIRouter
from ..dependencies.models import ModelDependency

router = APIRouter(tags=["model"])


@router.get("/info")
def model_info(model: ModelDependency):
    return str(model)
