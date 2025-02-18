from mlserver.types import InferenceErrorResponse


class InferenceError(BaseException):
    """Indicates an error returned by an inference endpoint."""

    def __init__(self, response: InferenceErrorResponse):
        super().__init__(response.error)
        self.response = response.model_copy()
