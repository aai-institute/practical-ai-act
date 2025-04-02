FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG MLFLOW_VERSION=2.20.0

ENV UV_LINK_MODE=copy
ENV UV_SYSTEM_PYTHON=1

EXPOSE 5000

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && \
    apt-get install -yqq --no-install-recommends tini

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install \
    mlflow==${MLFLOW_VERSION} \
    google-cloud-storage \
    azure-storage-blob \
    boto3 \
    psycopg2-binary \
    prometheus_flask_exporter

# Use tini to properly handle container termination
ENTRYPOINT [ "tini", "--" ]