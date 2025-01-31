from datetime import datetime
from pathlib import Path
from typing import Annotated

import duckdb
import pandas as pd
import requests
from fastapi import Depends, Request

from hr_assistant.util import BoundedJSONBuffer


def _make_entry(input_data, output_data, metadata):
    if not metadata:
        metadata = {}
    metadata["timestamp"] = datetime.now().isoformat()
    return {
        "input": input_data,
        "output": output_data,
        "metadata": metadata,
    }


class AbstractPredictionLogger:
    """Abstract base class for logging model input and output data."""

    def log(self, input_data, output_data, metadata: dict | None = None):
        """Append a log entry to the buffer."""
        raise NotImplementedError

    def flush(self):
        """Flush any remaining log entries to disk."""
        raise NotImplementedError


class PredictionLogger(AbstractPredictionLogger):
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

        entry = _make_entry(input_data, output_data, metadata)
        self._buffer.append(entry)

    def flush(self):
        """Flush any remaining log entries to disk."""
        self._buffer.flush()


class OpenSearchPredictionLogger(PredictionLogger):
    """POC implementation of a prediction logger that writes to an OpenSearch index."""

    def __init__(self, api_base: str, index: str, auth: tuple[str, str] | None = None):
        self._api_base = api_base
        self._index = index
        self._auth = auth

    def log(self, input_data, output_data, metadata: dict | None = None):
        entry = _make_entry(input_data, output_data, metadata)
        r = requests.put(
            f"{self._api_base}/{self._index}/_doc/{metadata['timestamp']}",
            json=entry,
            verify=False,
            auth=self._auth,
        )
        r.raise_for_status()

    def flush(self):
        pass


class DuckDBPredictionLogger(PredictionLogger):
    """POC implementation of a prediction logger that writes to a DuckDB database."""

    def __init__(self, db_path: Path, table_name: str):
        self._db_path = db_path
        self._table_name = table_name
        self._db = duckdb.connect(db_path)

        # JSON extension is required for storing JSON data
        self._db.execute("INSTALL json; LOAD json;")
        self._db.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (input JSON, output JSON, metadata JSON)"
        )

    def log(self, input_data, output_data, metadata: dict | None = None):
        entry = _make_entry(input_data, output_data, metadata)
        self._db.append(self._table_name, pd.DataFrame.from_records([entry]))

    def flush(self):
        pass


def get_request_logger(request: Request) -> PredictionLogger:
    return request.app.state.request_logger


PredictionLoggerDependency = Annotated[PredictionLogger, Depends(get_request_logger)]
