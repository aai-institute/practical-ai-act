<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_images/logos/ai-compliance-guide-simple-dark.svg">
  <img src="docs/_images/logos/ai-compliance-guide-simple.svg">
</picture>

This repository contains an implementation of a high-risk AI system as per Chapter III of the EU Artificial Intelligence Act.
It demonstrates how different personas, especially providers of AI systems, can design their systems to ensure compliance with the AI Act.

The showcase is built as a machine learning pipeline, capturing the continuous nature of the ML lifecycle from data sourcing and processing to model training, deployment, inference, and monitoring in production.
All tools used in this project were selected with a modular software stack in mind, allowing readers to switch out components to their liking with little effort for their own use cases.
All software tools used in this showcase are open-source.

## Setting up the environment

The project uses [uv](https://github.com/astral-sh/uv) as a package manager.
Follow the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) to make uv available on your machine.

## Build documentation

To build and serve the documentation locally, run the following command in your terminal:

```console
uv run --group docs mkdocs serve
```

Once the server is up, the documentation will be available at <http://127.0.0.1:8000/>.

## Linting and testing

This repository contains a pre-commit configuration.
To ensure that changes conform to the rules, run `uv run pre-commit run --all-files` after staging your changes.
To run the project's test suite, you can use the `uv run pytest` command.

## A simple example

Change to the project's directory, and start an mlflow server in a terminal:

```
uv run mlflow server --host 127.0.0.1 --port 5000
```

Then, proceed to train a simple classifier by doing the following:

```
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 PYTHONPATH=src uv run python scripts/run_train_classifier.py
```

In a different terminal, start the FastAPI app:

```
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 uv run --group deploy uvicorn --reload hr_assistant.main:app
```

You can make a simple request to the app by running the following Python script:

```
python scripts/run_simple_request.py
```

Or, to fire off a batch of inference requests at once, run:

```
python scripts/fill_record_db.py
```

## Docker Compose deployment

The `deploy/compose.local.yml` Docker Compose stack comprises the following base components:

- **Minio** for block storage
- **MLflow** for experiment tracking & model registry
  - Accessible at <http://localhost:50000> (non-standard port to prevent clashes with macOS AirDrop and Colima)
  - Prometheus metrics exposed at `/metrics`
- **lakeFS** data lake, backed by MinIO
  - Accessible at <http://localhost:8000>

The `serve` profile of the Docker Compose stack deploys the ML model inference server, main application, and monitoring components:

- **FastAPI application**:
  - Accessible at <http://localhost:8001>, [OpenAPI docs](http://localhost:8001/docs)
  - Automatic watch for changes with hot reloading (needs Docker Compose `--watch/-w` flag)
  - Calls inference server REST endpoint in Docker Compose
  - Prometheus metrics endpoint at `/metrics`
- **MLServer**-based inference server (with a custom Docker container containing the inference-time dependencies), model fetched from MLflow model registry
  - OIP REST/gRPC endpoints at port 8080/8081
  - Prometheus metrics endpoint at port 8082
- **Prometheus & Grafana** for monitoring
  - Automatic discovery of Prometheus scrape targets based on `prometheus.` labels on containers
  - Grafana: <http://localhost:3001>, credentials `admin/admin`
  - Predefined Grafana dashboards for MLflow, the FastAPI app, and the inference server

The `dagster` profile contains the following:

- **Dagster Daemon** and **Webserver**, based on a common base image (`deploy/dagster/Dockerfile`)
- The **user code location** image, containing the assets, and used to launch executions (see `deploy/dagster/Dockerfile.salary_prediction`)

In order to train a model, start the basic stack using:

```
docker compose -f deploy/compose.local.yml up
```

You can then log your MLflow experiments/models to MLflow (<http://localhost:50000>).

The `model` service needs a registered version of the `salary-predictor` model in the MLflow registry to start.
The model to be loaded can be customized through the `MLSERVER_MODEL_URI` environment variable (defaults to `models:/salary-predictor/latest`).

The FastAPI application containing the demo for the use case is exposed at <http://localhost:8001>.

In order to start the serving parts of the Docker Compose stack, specify the `serve` profile:

```
docker compose -f deploy/compose.local.yml --profile serve up -w
```

## Caveats when running on Colima

Colima needs to be started with the `--network-address` switch to allow the model container to reach the MLflow server on the host.
To do this, run `colima start <options> --network-address`.

## Acknowledgment
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_images/logos/baiaa-logo.svg">
  <img src="docs/_images/logos/baiaa-logo-black.svg">
</picture>
The Bavarian AI Act Accelerator is a two-year project funded by the Bavarian State Ministry of Digital Affairs to support SMEs, start-ups, and the public sector in Bavaria in complying with the EU AI Act. Under the leadership of the appliedAI Institute for Europe and in collaboration with Ludwig Maximilian University, the Technical University of Munich, and the Technical University of Nuremberg, training, resources, and events are being offered. The project objectives include reducing compliance costs, shortening the time to compliance, and strengthening AI innovation. To achieve these objectives, the project is divided into five work packages: project management, research, education, tools and infrastructure, and community.
