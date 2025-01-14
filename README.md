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