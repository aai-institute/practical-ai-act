from typing import cast

import duckdb
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import Response

from hr_assistant.api.exceptions import InferenceError
from hr_assistant.dependencies.logging import (
    PredictionLoggerDependency,
    SQLitePredictionLogger,
)
from hr_assistant.dependencies.models import InferenceClientDependency


class ModelInput(BaseModel):
    A_SEX: int
    A_ENRLW: int
    A_FTPT: int
    A_HSCOL: int
    A_MARITL: int
    P_STAT: int
    PECERT1: int
    PEHSPNON: int
    PRDTHSP: int
    PRDASIAN: int
    PRDTRACE: int
    PENATVTY: int
    PRCITSHP: int
    PRDISFLG: int
    A_LFSR: int
    A_CLSWKR: int
    A_FTLF: int
    A_UNMEM: int
    A_UNTYPE: int
    PRUNTYPE: int
    A_WKSTAT: int
    INDUSTRY: int
    CLWK: int
    A_MJIND: int
    A_MJOCC: int
    PEMLR: int
    ERN_SRCE: int
    COV: int
    HEA: int
    A_AGE: int
    A_WKSLK: int
    WKSWORK: int
    A_USLHRS: int
    HRSWK: int
    A_HRS1: int
    NOEMP: int
    A_GRSWK: int
    A_HRSPAY: int
    ERN_VAL: int
    WAGEOTR: int
    AGI: int
    A_FNLWGT: int
    A_HGA: int


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
        result = await inference_client.predict(request)
        return Response(content=result.to_json(orient="records"))
    except InferenceError as e:
        raise HTTPException(status_code=500, detail=e.response.error) from e


# FIXME: This is an ugly workaround to enable building the Dagster sensor
@router.get("/logs")
async def inference_logs(logger: PredictionLoggerDependency):
    db_path = cast(SQLitePredictionLogger, logger)._db_path
    with duckdb.connect() as db:
        db.query(f"ATTACH '{db_path}' (TYPE SQLITE);")
        df = db.query(
            "SELECT * FROM predictions.inference_requests req LEFT JOIN predictions.inference_responses resp ON (req.id == resp.id)"
        ).df()
        return Response(df.to_csv(), media_type="application/csv")
