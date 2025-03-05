import enum
import json
import logging
import sqlite3
import threading
import uuid
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Annotated

import duckdb
import httpx
import pandas as pd
import psycopg2
import psycopg2.extras
import requests
from fastapi import Depends, Request
from mlserver.types import (
    InferenceErrorResponse,
    InferenceRequest,
    InferenceResponse,
)
from pydantic import BaseModel

from hr_assistant.dependencies.db import db_conn
from hr_assistant.util import BoundedJSONBuffer


def _make_event_id() -> str:
    """Create a globally unique event ID."""
    return str(uuid.uuid4())


def _json_list(arr: Sequence[BaseModel]) -> str:
    """Serialize a sequence of Pydantic models to JSON"""
    return json.dumps([el.model_dump() for el in arr])


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


class OpenSearchPredictionLogger(AbstractPredictionLogger):
    """POC implementation of a prediction logger that writes to an OpenSearch index."""

    def __init__(
        self,
        api_base: str,
        index: str,
        auth: tuple[str, str] | None = None,
    ):
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


class DuckDBPredictionLogger(AbstractPredictionLogger):
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


class SQLitePredictionLogger(AbstractPredictionLogger):
    """POC implementation of a prediction logger that writes to a SQLite database.

    Log entries are tuples of Open Inference Protocol inference requests and responses.

    The implementation is thread-safe and uses a lock to ensure that multiple threads
    can write to the database without conflicts.
    """

    class Tables(enum.StrEnum):
        REQUEST = "inference_requests"
        RESPONSE = "inference_responses"

    def __init__(
        self,
        db_path: str = ":memory:",
    ):
        self._db_path = db_path
        self._lock = threading.RLock()
        self._db = sqlite3.connect(db_path, check_same_thread=False)

        # Table schemas according to the Open Inference Protocol REST endpoint specification for inference
        # https://github.com/kserve/open-inference-protocol/blob/main/specification/protocol/inference_rest.md

        request_schema = {
            "id": "TEXT PRIMARY KEY NOT NULL",
            "parameters": "JSONB",
            "inputs": "JSONB",
            "outputs": "JSONB",
        }
        response_schema = {
            "model_name": "TEXT",
            "model_version": "TEXT",
            "id": "TEXT PRIMARY KEY NOT NULL",
            "parameters": "JSONB",
            "outputs": "JSONB",
        }

        tables = {
            self.Tables.REQUEST: request_schema,
            self.Tables.RESPONSE: response_schema,
        }

        for table_name, schema in tables.items():
            with self._lock:
                schema_str = ", ".join([
                    f"{name} {typ}" for name, typ in schema.items()
                ])
                logging.info(f"Creating table {table_name} with schema {schema_str}")
                self._db.execute(
                    f"CREATE TABLE IF NOT EXISTS {table_name} ({schema_str})"
                )

    def log(
        self,
        input_data: InferenceRequest,
        output_data: InferenceResponse | InferenceErrorResponse,
        metadata=None,
    ):
        with self._lock:
            self._db.execute(
                f"INSERT INTO {self.Tables.REQUEST} VALUES (?, ?, ?, ?)",
                (
                    input_data.id,
                    input_data.parameters.model_dump_json(),
                    _json_list(input_data.inputs),
                    _json_list(input_data.outputs) if input_data.outputs else None,
                ),
            )

            if isinstance(output_data, InferenceResponse):
                self._db.execute(
                    f"INSERT INTO {self.Tables.RESPONSE} VALUES (?, ?, ?, ?, ?)",
                    (
                        output_data.model_name,
                        output_data.model_version,
                        output_data.id,
                        output_data.parameters.model_dump_json(),
                        _json_list(output_data.outputs),
                    ),
                )
            self._db.commit()

    def flush(self):
        pass


class PgSQLPredictionLogger(AbstractPredictionLogger):
    """POC implementation of a prediction logger that writes to a PostgreSQL database.

    Log entries are tuples of Open Inference Protocol inference requests and responses.
    """

    class Tables(enum.StrEnum):
        REQUEST = "inference_requests"
        RESPONSE = "inference_responses"
        ERROR = "inference_errors"
        METADATA = "inference_metadata"

    def __init__(
        self,
        db_conn: Annotated[psycopg2.extensions.connection, Depends(db_conn)],
    ):
        self._db_conn = db_conn

        request_schema = {
            "id": "TEXT PRIMARY KEY NOT NULL",
            "parameters": "JSONB",
            "inputs": "JSONB",
            "outputs": "JSONB",
        }
        response_schema = {
            "model_name": "TEXT",
            "model_version": "TEXT",
            "id": "TEXT PRIMARY KEY NOT NULL",
            "parameters": "JSONB",
            "outputs": "JSONB",
        }
        error_schema = {
            "id": "TEXT PRIMARY KEY NOT NULL",
            "error": "TEXT",
            "response": "JSONB",
        }
        metadata_schema = {
            "id": "TEXT PRIMARY KEY NOT NULL",
            "metadata": "JSONB",
        }

        tables = {
            self.Tables.REQUEST: request_schema,
            self.Tables.RESPONSE: response_schema,
            self.Tables.ERROR: error_schema,
            self.Tables.METADATA: metadata_schema,
        }

        with self._db_conn.cursor() as cur:
            for table_name, schema in tables.items():
                schema_str = ", ".join([
                    f"{name} {typ}" for name, typ in schema.items()
                ])
                logging.info(f"Creating table {table_name} with schema {schema_str}")
                cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema_str})")
            cur.connection.commit()

    def _log_request(self, cur: psycopg2.extensions.cursor, request: InferenceRequest):
        cur.execute(
            f"INSERT INTO {self.Tables.REQUEST} VALUES (%s, %s, %s, %s)",
            (
                request.id,
                request.parameters.model_dump_json(),
                _json_list(request.inputs),
                _json_list(request.outputs) if request.outputs else None,
            ),
        )

    def _log_response(
        self,
        cur: psycopg2.extensions.cursor,
        request_id: str,
        response: InferenceResponse | InferenceErrorResponse,
        raw_response: httpx.Response | None = None,
    ):
        if isinstance(response, InferenceResponse):
            cur.execute(
                f"INSERT INTO {self.Tables.RESPONSE} VALUES (%s, %s, %s, %s, %s)",
                (
                    response.model_name,
                    response.model_version,
                    response.id,
                    response.parameters.model_dump_json(),
                    _json_list(response.outputs),
                ),
            )

        if isinstance(response, InferenceErrorResponse):
            response_info = {
                "status_code": raw_response.status_code,
                "url": str(raw_response.url),
                "duration": raw_response.elapsed.total_seconds(),
                "method": raw_response.request.method,
                "headers": dict(raw_response.headers),
                "body": raw_response.text,
            }
            cur.execute(
                f"INSERT INTO {self.Tables.ERROR} VALUES (%s, %s, %s)",
                (
                    request_id,
                    response.error,
                    psycopg2.extras.Json(response_info),
                ),
            )

    def _log_metadata(
        self, cur: psycopg2.extensions.cursor, request_id: str, metadata: dict
    ):
        if not metadata:
            return
        cur.execute(
            f"INSERT INTO {self.Tables.METADATA} VALUES (%s, %s)",
            (
                request_id,
                psycopg2.extras.Json(metadata),
            ),
        )

    def log(
        self,
        input_data: InferenceRequest,
        output_data: InferenceResponse | InferenceErrorResponse,
        raw_response: httpx.Response | None = None,
        metadata=None,
    ):
        with self._db_conn.cursor() as cur:
            self._log_request(cur, input_data)
            self._log_response(cur, input_data.id, output_data, raw_response)
            self._log_metadata(cur, input_data.id, metadata)
            cur.connection.commit()


def get_request_logger(request: Request) -> PredictionLogger:
    return request.state.request_logger


PredictionLoggerDependency = Annotated[
    AbstractPredictionLogger, Depends(PgSQLPredictionLogger)
]
