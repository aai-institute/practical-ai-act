ARG UV_BASE_IMAGE_TAG=python3.13-bookworm-slim
FROM ghcr.io/astral-sh/uv:${UV_BASE_IMAGE_TAG}

ARG MLFLOW_VERSION=2.20.0

ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install \
    mlflow==${MLFLOW_VERSION} \
    google-cloud-storage \
    azure-storage-blob \
    boto3 \
    psycopg2-binary