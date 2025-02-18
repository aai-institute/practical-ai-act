FROM python:3.12 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --group deploy

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --group deploy

FROM python:3.12-slim

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

CMD ["/app/.venv/bin/uvicorn", "--reload", "hr_assistant.main:app", "--host", "0.0.0.0"]