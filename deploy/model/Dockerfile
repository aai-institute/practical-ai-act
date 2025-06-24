FROM python:3.12 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Cannot symlink into the cache mount directory, need to copy installed files instead
ENV UV_LINK_MODE=copy

WORKDIR /app

ARG MLFLOW_TRACKING_URI
ENV MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI

ARG MODEL_NAME
ENV MODEL_NAME=$MODEL_NAME

ARG MODEL_VERSION=latest
ENV MODEL_VERSION=$MODEL_VERSION

ENV MODEL_URI="models:/${MODEL_NAME}/${MODEL_VERSION}"
ENV EXTRA_PACKAGES='mlserver>=1.7.0 mlserver-sklearn>=1.7.0 shap>0.47'

# Download the model artifacts and install the model serving Python requirements
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=download_model_artifacts.py,target=/download_model_artifacts.py \
  PYTHONUNBUFFERED=1 uv run --with=mlflow python /download_model_artifacts.py && \
  ls -lh /explainer && \
  uv venv --seed && \
  uv pip install -r /model/artifacts/requirements.txt ${EXTRA_PACKAGES}

FROM python:3.12-slim

COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY * /app/
COPY --from=builder --chown=app:app /model /model
COPY --from=builder --chown=app:app /explainer /explainer

ARG MODEL_NAME
ENV MLSERVER_MODEL_NAME=$MODEL_NAME

ARG MODEL_VERSION=latest
ENV MLSERVER_MODEL_VERSION=$MODEL_VERSION
ENV MLSERVER_MODEL_URI="file:///model/artifacts/model.pkl"

EXPOSE 8080 8081 8082

# Run the application
CMD ["/app/.venv/bin/mlserver", "start", "/app"]
