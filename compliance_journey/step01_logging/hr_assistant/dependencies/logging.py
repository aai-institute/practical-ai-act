import json
import sqlite3
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Annotated

import duckdb
import pandas as pd
import requests
from fastapi import Depends, Request

from ..util import BoundedJSONBuffer


def _make_event_id() -> str:
    """Create a globally unique event ID."""
    return str(uuid.uuid4())


def _make_entry(input_data, output_data, metadata):
    """Create a log entry with the given input, output, and metadata.

    The entry includes a globally unique event ID."""

    if not metadata:
        metadata = {}
    metadata["timestamp"] = datetime.now().isoformat()
    return {
        "id": _make_event_id(),
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
            f"CREATE TABLE IF NOT EXISTS {table_name} (id VARCHAR PRIMARY KEY, input JSON, output JSON, metadata JSON)"
        )

    def log(self, input_data, output_data, metadata: dict | None = None):
        entry = _make_entry(input_data, output_data, metadata)
        self._db.append(self._table_name, pd.DataFrame.from_records([entry]))

    def flush(self):
        pass


def get_request_logger(request: Request) -> PredictionLogger:
    return request.app.state.request_logger


PredictionLoggerDependency = Annotated[PredictionLogger, Depends(get_request_logger)]


class SQLitePredictionLogger(PredictionLogger):
    """POC implementation of a prediction logger that writes to a SQLite database.

    Optionally, entires can be committed to disk after a specified number of records have been added.

    The implementation is thread-safe and uses a lock to ensure that multiple threads
    can write to the database without conflicts.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        table_name: str = "predictions",
        capacity: int = -1,
    ):
        self._db_path = db_path
        self._lock = threading.RLock()

        self._table_name = table_name
        self._db = sqlite3.connect(db_path, check_same_thread=False)

        self._db.execute(
            f"CREATE TABLE IF NOT EXISTS {self._table_name} (id TEXT PRIMARY KEY, input JSONB, output JSONB, metadata JSONB)"
        )

        self._capacity = capacity
        self._pending_records = 0

    def _flush_if_needed(self):
        if self._capacity < 0 or (
            self._capacity > 0 and self._pending_records >= self._capacity
        ):
            self.flush()

    def log(self, input_data, output_data, metadata=None):
        entry = _make_entry(input_data, output_data, metadata)
        with self._lock:
            self._db.execute(
                f"INSERT INTO {self._table_name} VALUES (?, ?, ?, ?)",
                (
                    entry["id"],
                    json.dumps(input_data),
                    json.dumps(output_data),
                    json.dumps(metadata),
                ),
            )
            self._pending_records += 1
            self._flush_if_needed()

    def flush(self):
        with self._lock:
            self._db.commit()
            self._pending_records = 0
