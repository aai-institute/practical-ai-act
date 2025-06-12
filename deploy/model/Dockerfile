FROM python:3.12 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Cannot symlink into the cache mount directory, need to copy installed files instead
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY download_model_artifacts.py /

# Minimal dependencies to access MLflow model registry
RUN --mount=type=cache,target=/root/.cache/uv \
  uv venv --seed && \
  uv pip install mlflow 'mlserver>=1.7.0' 'mlserver-sklearn>=1.7.0' 'shap>0.47'

ARG MLFLOW_TRACKING_URI
ENV MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI

ARG MODEL_NAME
ENV MODEL_NAME=$MODEL_NAME

ARG MODEL_VERSION=latest
ENV MODEL_VERSION=$MODEL_VERSION

# Download the model artifacts and install the model serving Python requirements
# FIXME: Exclude `hr-assistant` package since its code will be added to PYTHONPATH at runtime from the model artifacts
RUN --mount=type=cache,target=/root/.cache/uv \
  PYTHONUNBUFFERED=1 uv run python /download_model_artifacts.py && \
  grep -v "hr-assistant" /model/artifacts/requirements.txt | uv pip install -r -

FROM python:3.12-slim

COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY * /app/
COPY --from=builder --chown=app:app /model /model

ARG MODEL_NAME
ENV MLSERVER_MODEL_NAME=$MODEL_NAME

ARG MODEL_VERSION=latest
ENV MLSERVER_MODEL_VERSION=$MODEL_VERSION

ENV MLSERVER_MODEL_URI="file:///model/artifacts/model.pkl"
# FIXME: Extract code paths from model metadata
ENV PYTHONPATH=/model/artifacts/code

EXPOSE 8080 8081 8082

# Run the application
CMD ["/app/.venv/bin/mlserver", "start", "/app"]
