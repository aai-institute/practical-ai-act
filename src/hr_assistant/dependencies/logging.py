import enum
import json
import logging
from collections.abc import Sequence
from typing import Annotated

import httpx
import psycopg2
import psycopg2.extras
from fastapi import Depends
from mlserver.types import (
    InferenceErrorResponse,
    InferenceRequest,
    InferenceResponse,
)
from pydantic import BaseModel

from hr_assistant.dependencies.db import db_conn


def _json_list(arr: Sequence[BaseModel]) -> str:
    """Serialize a sequence of Pydantic models to JSON"""
    return json.dumps([el.model_dump() for el in arr])


class AbstractPredictionLogger:
    """Abstract base class for logging model input and output data."""

    def log(self, input_data, output_data, metadata: dict | None = None):
        """Append a log entry to the buffer."""
        raise NotImplementedError

    def flush(self):
        """Flush any remaining log entries to disk."""
        raise NotImplementedError


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
            "timestamp": "TIMESTAMPTZ DEFAULT NOW()",
            "parameters": "JSONB",
            "inputs": "JSONB",
            "outputs": "JSONB",
            "raw_request": "JSONB",
        }
        response_schema = {
            "model_name": "TEXT",
            "model_version": "TEXT",
            "id": "TEXT PRIMARY KEY NOT NULL",
            "timestamp": "TIMESTAMPTZ DEFAULT NOW()",
            "parameters": "JSONB",
            "outputs": "JSONB",
            "raw_response": "JSONB",
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
            f"INSERT INTO {self.Tables.REQUEST} (id, parameters, inputs, outputs, raw_request) VALUES (%s, %s, %s, %s, %s)",
            (
                request.id,
                request.parameters.model_dump_json(),
                _json_list(request.inputs),
                _json_list(request.outputs) if request.outputs else None,
                request.model_dump_json(),
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
                f"INSERT INTO {self.Tables.RESPONSE} (model_name, model_version, id, parameters, outputs, raw_response) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    response.model_name,
                    response.model_version,
                    response.id,
                    response.parameters.model_dump_json(),
                    _json_list(response.outputs),
                    response.model_dump_json(),
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
                f"INSERT INTO {self.Tables.ERROR} (id, error, response) VALUES (%s, %s, %s)",
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
            f"INSERT INTO {self.Tables.METADATA} (id, metadata) VALUES (%s, %s)",
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

    def fetch(self, request_id: str):
        """Fetch the request, response, error, and metadata for a given request ID."""

        with self._db_conn.cursor() as cur:
            cur.execute(
                f"SELECT raw_request FROM {self.Tables.REQUEST} WHERE id = %s",
                (request_id,),
            )
            request = (
                InferenceRequest.model_validate(cur.fetchone()[0])
                if cur.rowcount
                else None
            )

            cur.execute(
                f"SELECT raw_response FROM {self.Tables.RESPONSE} WHERE id = %s",
                (request_id,),
            )
            response = (
                InferenceResponse.model_validate(cur.fetchone()[0])
                if cur.rowcount
                else None
            )

            cur.execute(
                f"SELECT id, error FROM {self.Tables.ERROR} WHERE id = %s",
                (request_id,),
            )
            error_data = cur.fetchone()
            error = (
                InferenceErrorResponse.model_validate(
                    id=error_data[0], error=error_data[1]
                )
                if error_data
                else None
            )

            cur.execute(
                f"SELECT * FROM {self.Tables.METADATA} WHERE id = %s",
                (request_id,),
            )
            metadata = cur.fetchone() if cur.rowcount else None
        return request, response, error, metadata


PredictionLoggerDependency = Annotated[
    PgSQLPredictionLogger, Depends(PgSQLPredictionLogger)
]
