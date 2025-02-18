from fastapi import APIRouter, HTTPException

from hr_assistant.dependencies.models import InferenceClientDependency

router = APIRouter(tags=["model"])


@router.get("/info")
async def model_info(inference_client: InferenceClientDependency):
    resp, success = await inference_client.metadata()
    if not success:
        raise HTTPException(detail=resp.error, status_code=500)
    return resp
