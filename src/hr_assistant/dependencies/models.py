from functools import partial
from typing import Annotated

import fastapi
import httpx
import pandas as pd
from fastapi import Depends
from mlserver.codecs import PandasCodec
from mlserver.types import (
    InferenceErrorResponse,
    InferenceRequest,
    InferenceResponse,
    MetadataModelErrorResponse,
    MetadataModelResponse,
)

from hr_assistant.api.exceptions import InferenceError
from hr_assistant.config import INFERENCE_ENDPOINT
from hr_assistant.dependencies.logging import PredictionLoggerDependency


class OpenInferenceProtocolClient:
    """
    Client for inference servers compatible with the Open Inference protocol.
    """

    def __init__(
        self,
        base_url: str,
        model_name: str,
        request: fastapi.Request,
        logger: PredictionLoggerDependency,
    ) -> None:
        self._httpx = httpx.AsyncClient(base_url=base_url)
        self._model_name = model_name
        self._request = request
        self._logger = logger

    def build_request(self, input_data: pd.DataFrame) -> InferenceRequest:
        request = PandasCodec.encode_request(input_data, use_bytes=False)
        request.id = self._request.state.request_id
        return request

    async def metadata(
        self,
    ) -> tuple[MetadataModelResponse | MetadataModelErrorResponse, bool]:
        """Fetch model info from the inference server"""

        resp = await self._httpx.get(f"/v2/models/{self._model_name}")
        if "error" in resp.json():
            return MetadataModelErrorResponse(**resp.json()), False
        else:
            return MetadataModelResponse(**resp.json()), True

    async def predict(self, request: InferenceRequest) -> pd.DataFrame:
        """Perform and log an inference request."""

        resp = await self._httpx.post(
            f"/v2/models/{self._model_name}/infer", content=request.model_dump_json()
        )
        data = resp.json()
        # No raise_for_status() since the Open Inference Protocol returns a custom error response

        response: InferenceResponse | InferenceErrorResponse

        if "error" in data:
            response = InferenceErrorResponse(**data)
            success = False
        else:
            response = InferenceResponse(**data)
            success = True

        # Log inference request/response pair
        self._logger.log(request, response)

        if not success:
            raise InferenceError(response)
        return PandasCodec.decode_response(response)


InferenceClientDependency = Annotated[
    OpenInferenceProtocolClient,
    Depends(
        partial(
            OpenInferenceProtocolClient,
            base_url=INFERENCE_ENDPOINT,
            model_name="mlflow-model",  # FIXME: `mlflow models serve` uses hardcoded name
        )
    ),
]
