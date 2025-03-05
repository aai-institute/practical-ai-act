from mlserver.types import InferenceErrorResponse


class InferenceError(BaseException):
    """Indicates an error returned by an inference endpoint."""

    def __init__(
        self, response: InferenceErrorResponse | None = None, message: str | None = None
    ):
        if response is None:
            super().__init__(message)
            self.response = None
        else:
            super().__init__(response.error)
            self.response = response.model_copy()

    @property
    def message(self) -> str:
        return str(self)
