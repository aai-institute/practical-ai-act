import os

import mlflow
from dagster import AssetExecutionContext, ConfigurableResource, InitResourceContext

from income_prediction.utils.dagster import extract_run_id
from income_prediction.utils.mlflow import start_mlflow_run


class MlflowSession(ConfigurableResource):
    """Manages MLflow sessions for tracking experiments within a Dagster pipeline.

    Attributes
    ----------
    tracking_url : str
        URL of the MLflow tracking server.
    username : Optional[str]
        Username for accessing the MLflow server, if required.
    password : Optional[str]
        Password for accessing the MLflow server, if required.
    experiment : str
        Name of the MLflow experiment to log runs to.
    run_name_prefix : str
        Prefix to prepend to run names.
    """

    tracking_url: str
    username: str | None
    password: str | None

    experiment: str
    run_name_prefix: str = ""

    def setup_for_execution(self, context: InitResourceContext) -> None:
        """Configures MLflow tracking settings, including authentication credentials and the tracking server URI.

        Parameters
        ----------
        context : InitResourceContext
            The initialization context provided by Dagster.
        """

        # mlflow expects the username and password as environment variables
        if self.username:
            os.environ.setdefault("MLFLOW_TRACKING_USERNAME", self.username)
        if self.password:
            os.environ.setdefault("MLFLOW_TRACKING_PASSWORD", self.password)

        mlflow.set_tracking_uri(self.tracking_url)
        mlflow.set_experiment(self.experiment)

    def start_run(
        self,
        context: AssetExecutionContext,
        run_name: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> mlflow.ActiveRun:
        """Starts an MLflow run, assigning a run_name and relevant tags.

        Parameters
        ----------
        context : AssetExecutionContext
            Dagster execution context for retrieving the run ID.
        run_name : str, optional
            Custom name for the MLflow run. If not provided, it is derived from the Dagster run ID.
        tags : dict[str,str], optional
            Additional metadata tags for the MLflow run.
        """
        run_id = extract_run_id(context)

        if not run_name:
            run_name = f"{self.run_name_prefix}{run_id}"

        if tags is None:
            tags = {}

        tags["dagster.run_id"] = run_id

        return start_mlflow_run(run_name, tags=tags)
