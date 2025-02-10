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

Change to  the project's directory.

Start a mlflow server in a terminal:
```
uv run mlflow server --host 127.0.0.1 --port 8080
```

Train a simple classifier:

```
MLFLOW_TRACKING_URI=http://127.0.0.1:8080 PYTHONPATH=src uv run python scripts/run_train_classifier.py
```

In a different terminal start the fastAPI app:
```
MLFLOW_TRACKING_URI=http://127.0.0.1:8080 uv run --group deploy fastapi dev src/hr_assistant/main.py
```

Run a simple request to the app:

```
python scripts/run_simple_request.py
```