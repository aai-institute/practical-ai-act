# twai-pipeline

## Setting up the environment

The project uses [uv](https://github.com/astral-sh/uv) as a package
manager. Follow the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
to have uv available on your machine.

## Build documentation

In your terminal:

```
uv run --group docs mkdocs serve
```

Once the server is up, the documentation should be available on port [8000](http://127.0.0.1:8000/).

## Simple example

Change to the project's directory.

Start a mlflow server in a terminal:

```
uv run mlflow server --host 127.0.0.1 --port 5000
```

Train a simple classifier:

```
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 PYTHONPATH=src uv run python scripts/run_train_classifier.py
```

In a different terminal start the FastAPI app:

```
MLFLOW_TRACKING_URI=http://127.0.0.1:5000 uv run --group deploy uvicorn --reload hr_assistant.main:app
```

Run a simple request to the app:

```
python scripts/run_simple_request.py
```

Or, to fire off a batch of inference requests at once:

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

In order to train a model, start the basic stack using:

```
docker compose -f deploy/compose.local.yml up
```

You can then log your MLflow experiments/models to MLflow (<http://localhost:50000>).

The `model` service needs a registered version of the `xgboost-classifier` model in the MLflow registry to start.
The model to be loaded can be customized through the `MLSERVER_MODEL_URI` environment variable (defaults to `models:/xgboost-classifier/latest`).

The FastAPI application containing the demo for the use case is exposed at <http://localhost:8001>.

In order to start the serving parts of the Docker Compose stack, specify the `serve` profile:

```
docker compose -f deploy/compose.local.yml --profile serve up -w
```
