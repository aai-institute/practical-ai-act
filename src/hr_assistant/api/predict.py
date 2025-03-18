import io
import json

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from mlserver.codecs import NumpyCodec, StringCodec
from pydantic import BaseModel
from starlette.responses import Response

from hr_assistant.api.exceptions import InferenceError
from hr_assistant.dependencies.logging import PredictionLoggerDependency
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
        # Making a prediction will automatically record explanations in the inference log
        result = await inference_client.predict(request)
        predict = result["predict"]
        predict_proba = result["predict_proba"]

        df = pd.concat(
            [
                pd.Series(predict.ravel(), name="class"),
                pd.Series(predict_proba.tolist(), name="probabilities"),
            ],
            axis=1,
        )
        return Response(content=df.to_json(orient="records"))
    except InferenceError as e:
        raise HTTPException(status_code=500, detail=e.message) from e


@router.get(
    "/explain/{request_id}",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
async def explain_prediction(
    request_id: str,
    logger: PredictionLoggerDependency,
):
    # Fetch the explanation data from the inference log

    req, resp, err, _ = logger.fetch(request_id)
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")

    if err:
        raise HTTPException(
            status_code=404,
            detail="Request resulted in error, no explanation possible.",
        )

    explanation_data = next((o for o in resp.outputs if o.name == "explain"), None)
    if explanation_data is None:
        raise HTTPException(status_code=404, detail="Explanation data not found")

    decoded = StringCodec.decode_output(explanation_data)
    decoded = json.loads(decoded[0])

    # Restore numpy arrays in explanation data
    decoded["values"] = np.array(decoded["values"])
    decoded["base_values"] = np.array(decoded["base_values"])
    decoded["data"] = np.array(decoded["data"])

    import shap.plots

    explanation = shap.Explanation(**decoded)

    # Use waterfall plot for single-instance predictions, summary plot for batch predictions
    if len(explanation) == 1:
        # Restore predictions
        predictions = next((o for o in resp.outputs if o.name == "predict"), None)
        predictions = NumpyCodec.decode_output(predictions).ravel()
        print(predictions.shape)

        # Plot feature importance on the predicted class
        predicted_class = predictions[0]
        data = explanation[0, :, predicted_class]
        num_features = 10
        ax = shap.plots.waterfall(
            data,
            max_display=num_features,
            show=False,
        )

        # HACK: Manually rescale the plot to fit the feature names and values
        ax.get_figure().set_size_inches(15, num_features * 0.5 + 1.5)
    else:
        ax = shap.summary_plot(
            explanation.values,
            explanation.data,
            show=False,
            feature_names=explanation.feature_names,
            plot_type="bar",
        )

    buf = io.BytesIO()
    ax.get_figure().savefig(buf, format="png")
    return Response(content=buf.getvalue(), media_type="image/png")
