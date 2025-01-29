from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import Depends, Request

from hr_assistant.util import BoundedJSONBuffer


class PredictionLogger:
    """Log model input and output data to a JSONL file.

    To be used as a FastAPI dependency.

    Parameters
    ----------
    jsonl_path : Path
        The file path where the log entries will be stored.
    capacity : int
        The maximum number of log entries to keep in memory before flushing to disk.
        Defaults to 100.
    """

    def __init__(
        self,
        jsonl_path: Path,
        capacity: int = 100,
    ):
        self._buffer = BoundedJSONBuffer(jsonl_path, capacity=capacity)

    def log(self, input_data, output_data, metadata: dict | None = None):
        """Append a log entry to the buffer.

        The current timestamp is automatically added to the metadata."""

        if not metadata:
            metadata = {}

        metadata["timestamp"] = datetime.now().isoformat()

        self._buffer.append({
            "input": input_data,
            "output": output_data,
            "metadata": metadata,
        })


def get_request_logger(request: Request) -> PredictionLogger:
    return request.app.state.request_logger


PredictionLoggerDependency = Annotated[PredictionLogger, Depends(get_request_logger)]
