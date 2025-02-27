FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG DAGSTER_CORE_VERSION=1.10.2
ARG DAGSTER_LIB_VERSION=0.26.2

ENV UV_SYSTEM_PYTHON=1
ENV UV_LINK_MODE=copy

EXPOSE 3000

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install \
    dagster==${DAGSTER_CORE_VERSION} \
    dagster-graphql==${DAGSTER_CORE_VERSION} \
    dagster-webserver==${DAGSTER_CORE_VERSION} \
    dagster-postgres==${DAGSTER_LIB_VERSION} \
    dagster-docker==${DAGSTER_LIB_VERSION} \
    dagster-obstore==0.2.0

# Set $DAGSTER_HOME and copy dagster.yaml and workspace.yaml there
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p $DAGSTER_HOME

COPY deploy/dagster/dagster.yaml deploy/dagster/workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME
ENTRYPOINT ["uv", "run"]