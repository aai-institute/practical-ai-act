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

ARG NANNYML_ESTIMATOR
COPY deploy/nannyml/main.py .
COPY $NANNYML_ESTIMATOR ./nannyml_estimator.pkl
ENV NANNYML_ESTIMATOR=/app/nannyml_estimator.pkl

CMD ["/app/.venv/bin/uvicorn", "--reload", "main:app", "--host", "0.0.0.0", "--port", "4040"]
