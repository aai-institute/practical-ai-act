import mlflow
import mlflow.sklearn


def start_mlflow_run(
    run_name: str, tags: dict[str, str] | None = None
) -> mlflow.ActiveRun:
    """Starts a new MLflow run or retrieves an existing run with the specified run name.

    Parameters
    ----------
    run_name : str
        Name of the MLflow run.
    tags : dict[str, str], optional
        A dictionary of tags to associate with the MLflow run. Defaults to None.

    Returns
    -------
    mlflow.ActiveRun
        The active MLflow run.
    """

    if tags is None:
        tags = {}

    active_run = mlflow.active_run()
    if active_run:
        return active_run

    existing_runs = mlflow.search_runs(
        filter_string=f"attributes.`run_name`='{run_name}'", output_format="list"
    )

    if existing_runs:
        run_id = existing_runs[0].info.run_id
        return mlflow.start_run(run_id=run_id)

    return mlflow.start_run(run_name=run_name, tags=tags)
