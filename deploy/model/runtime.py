import json

import numpy as np
import shap
from mlserver.codecs import PandasCodec, StringCodec
from mlserver.errors import InferenceError
from mlserver.model import (
    InferenceRequest,
    RequestOutput,
    ResponseOutput,
)
from mlserver_sklearn import SKLearnModel
from mlserver_sklearn.sklearn import (
    PREDICT_FN_KEY,
    PREDICT_OUTPUT,
    PREDICT_PROBA_OUTPUT,
    PREDICT_TRANSFORM,
)
from mlserver_sklearn.sklearn import VALID_OUTPUTS as SKLEARN_OUTPUTS
from scipy.sparse import csr_matrix
from sklearn.pipeline import Pipeline

EXPLAIN_OUTPUT = "explain"
VALID_OUTPUTS = SKLEARN_OUTPUTS + [EXPLAIN_OUTPUT]


def _strip_prefix(s: str) -> str:
    """Remove the pipeline step prefix from a feature name."""
    return s.split("__")[-1]


def _serialize_explanation(expl: shap.Explanation) -> str:
    """Convert SHAP explanation into a serialized representation."""

    # Extract and serialize numerical data from the underlying slicer object,
    # wrapping Numpy arrays and sparse matrices into lists for JSON serialization.
    result = {}
    for k, v in expl._s.__dict__.items():
        # o is a reserved named in Slicer
        if k.startswith("_") or k == "o" or v is None:
            continue
        elif isinstance(v, np.ndarray):
            result[k] = v.tolist()
        elif isinstance(v, csr_matrix):
            result[k] = v.toarray().tolist()
        else:
            result[k] = v

    # Non-numerical data is stored on the explanation object itself
    for k in ["feature_names", "output_names"]:
        result[k] = getattr(expl, k, None)

    return json.dumps(result)


class ExplainableSKLearnModel(SKLearnModel):
    """MLModel implementation for scikit-learn models with explainability support.

    It extends ``SKLearnModel`` to provide SHAP-based explainability data in JSON format
    for the ``explain`` output type. The model must be a scikit-learn pipeline with a
    classifier as the final step."""

    explainer: shap.Explainer

    async def load(self):
        await super().load()

        if not isinstance(self._model, Pipeline):
            raise InferenceError(
                "ExplainableSKLearnModel only supports scikit-learn pipelines"
            )

        # Split the pipeline into a feature transformer and the model
        self.feature_pipeline = self._model[:-1]
        self.predictor = self._model[-1]

        # Construct SHAP explainer for the underlying XGboost model, using the transformed
        # feature names.This allows us to use a TreeExplainer for the SKlearn pipeline,
        # which otherwise can only use the slower PermutationExplainer.

        # Remove the pipeline step prefix from feature names for readability
        feature_names = [
            _strip_prefix(s) for s in self.feature_pipeline.get_feature_names_out()
        ]
        self.explainer = shap.TreeExplainer(self.predictor, feature_names=feature_names)

        return True

    def _explain(self, payload: InferenceRequest) -> ResponseOutput:
        decoded_request = self.decode_request(payload, default_codec=PandasCodec)
        transformed_request = self.feature_pipeline.transform(decoded_request)
        explanation = self.explainer(transformed_request)
        data = _serialize_explanation(explanation)
        return StringCodec.encode_output(EXPLAIN_OUTPUT, [data])

    def _get_model_outputs(self, payload: InferenceRequest) -> list[ResponseOutput]:
        outputs = []

        output_names = [o.name for o in payload.outputs]
        if EXPLAIN_OUTPUT in output_names:
            explain_output = self._explain(payload)
            outputs.append(explain_output)

        payload.outputs = [
            out for out in payload.outputs if out.name != EXPLAIN_OUTPUT
        ] or []
        outputs.extend(super()._get_model_outputs(payload))

        return outputs

    def _check_request(self, payload: InferenceRequest) -> InferenceRequest:
        # Copied and adapted from SKLearnModel to include extra output type for explainability
        if not payload.outputs:
            found_predict_fn = False
            if self.settings.parameters:
                if self.settings.parameters.extra:
                    if PREDICT_FN_KEY in self.settings.parameters.extra:
                        payload.outputs = [
                            RequestOutput(
                                name=self.settings.parameters.extra[PREDICT_FN_KEY]
                            )
                        ]
                        found_predict_fn = True
            # By default, only return the result of `predict()`
            if not found_predict_fn:
                payload.outputs = [RequestOutput(name=PREDICT_OUTPUT)]
        else:
            for request_output in payload.outputs:
                if request_output.name not in VALID_OUTPUTS:
                    raise InferenceError(
                        f"ExplainableSKLearnModel only supports '{PREDICT_OUTPUT}', "
                        f"'{PREDICT_PROBA_OUTPUT}', "
                        f"'{EXPLAIN_OUTPUT}', and "
                        f"'{PREDICT_TRANSFORM}' as outputs "
                        f"({request_output.name} was received)"
                    )

        # Regression models do not support `predict_proba`
        output_names = [o.name for o in payload.outputs]  # type: ignore
        if PREDICT_PROBA_OUTPUT in output_names:
            # Ensure model supports it
            maybe_regressor = self._model
            if isinstance(self._model, Pipeline):
                maybe_regressor = maybe_regressor.steps[-1][-1]

            if not hasattr(maybe_regressor, PREDICT_PROBA_OUTPUT):
                raise InferenceError(
                    f"{type(maybe_regressor)} models do not support "
                    f"'{PREDICT_PROBA_OUTPUT}"
                )

        return payload
