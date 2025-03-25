FROM python:3.12 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --group monitoring


FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

RUN apt-get update && \
  apt-get install -yqq --no-install-recommends libgomp1

COPY deploy/nannyml/main.py .

ARG NANNYML_ESTIMATOR
COPY $NANNYML_ESTIMATOR ./nannyml_estimator.pkl
ENV NANNYML_ESTIMATOR=/app/nannyml_estimator.pkl

ARG NANNYML_DRIFT_CALCULATOR
COPY $NANNYML_DRIFT_CALCULATOR ./nannyml_drift_calc.pkl
ENV NANNYML_DRIFT_CALCULATOR=/app/nannyml_drift_calc.pkl

CMD ["/app/.venv/bin/uvicorn", "--reload", "main:app", "--host", "0.0.0.0", "--port", "4040"]
