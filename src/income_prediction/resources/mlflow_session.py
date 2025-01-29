"""MLflow session management resource for tracking experiments from Dagster."""

import os
from typing import Optional

import mlflow
from dagster import AssetExecutionContext, ConfigurableResource, InitResourceContext

SHORT_RUN_ID_LENGTH = 8
"""Number of characters to include in the shortened version of the run ID."""


def get_run_id(context: AssetExecutionContext, short: bool = False) -> str:
    """Retrieves the run ID from the Dagster execution context, optionally as shortened version.

    Parameters
    ----------
    context : AssetExecutionContext
        The Dagster asset execution context, which provides information about the current run.
    short : bool, optional, default False
        If True, this function returns only the first `SHORT_RUN_ID_LENGTH` characters of the run ID.

    Returns
    -------
    str
        The run ID for the current execution. Returns a shortened version of `short` is True.
    """
    run_id = context.run.run_id
    return run_id[:SHORT_RUN_ID_LENGTH] if short else run_id


def get_asset_key(context: AssetExecutionContext) -> str:
    """Converts the asset keys to a user-readable string format.

    Parameters
    ----------
    context : AssetExecutionContext
        The Dagster asset execution context, which provides information about the asset key.

    Returns
    -------
    str
        A string representation of the asset key.
    """
    return context.asset_key.to_user_string()


class MlflowSession(ConfigurableResource):
    """Manages MLflow sessions for tracking experiments within a Dagster pipeline.

    Attributes
    ----------
    tracking_url : str
        The URL of the MLflow tracking server.
    username : Optional[str]
        The username for accessing the MLflow server, if required.
    password : Optional[str]
        The password for accessing the MLflow server, if required.
    experiment : str
        The name of the MLflow experiment to log runs to.

    """

    tracking_url: str
    username: Optional[str]
    password: Optional[str]
    experiment: str

    def setup_for_execution(self, context: InitResourceContext) -> None:
        """Configures MLflow tracking.

        This function configures the access credentials (if required), the tracking server, and the experiment name.

        Parameters
        ----------
        context : InitResourceContext
            The initialization context provided by Dagster.
        """

        # mlflow expects the username and password as environment variables
        if self.username:
            os.environ["MLFLOW_TRACKING_USERNAME"] = self.username
        if self.password:
            os.environ["MLFLOW_TRACKING_PASSWORD"] = self.password

        mlflow.set_tracking_uri(self.tracking_url)
        mlflow.set_experiment(self.experiment)

    def _get_run_name_from_context(self, context: AssetExecutionContext, run_name_prefix: Optional[str]) -> str:
        """Generates a run name based on the asset key and Dagster run ID.

        Parameters
        ----------
        context : AssetExecutionContext
            The Dagster execution context, which provides information about the asset and run ID.
        run_name_prefix : Optional[str]
            A prefix to prepend to a generated run name.

        Returns
        -------
        str
            The run name.
        """

        asset_key = get_asset_key(context)
        dagster_run_id = get_run_id(context, short=True)

        run_name = f"{asset_key}-{dagster_run_id}"
        if run_name_prefix is not None:
            run_name = f"{run_name_prefix}-{run_name}"

        return run_name

    def get_run(
        self,
        context: AssetExecutionContext,
        run_name_prefix: Optional[str] = None,
        tags: dict[str, str] | None = None,
    ) -> mlflow.ActiveRun:
        """Retrieves an existing MLflow run or starts a new one with the specified run name and tags.

        This method checks if an MLflow run is already active. If not, it searches for an existing run with the
        specified name. If no run is found, a new run is started and tagged with the Dagster-related information.

        Parameters
        ----------
        context : AssetExecutionContext
            The Dagster asset execution context, which provides information about the asset.
        run_name_prefix : Optional[str], default None
            A prefix to prepend to the MLflow run name.
        tags : dict[str, str], default {}
            A dictionary of tags to associate with the MLflow run. The Dagster run ID and asset name will be added to
            the tags automatically.

        Returns
        -------
        mlflow.ActiveRun
            An active MLflow run which can be used for tracking experiments.
        """
        run_name = self._get_run_name_from_context(context, run_name_prefix)

        active_run = mlflow.active_run()
        if active_run is None:
            current_runs = mlflow.search_runs(
                filter_string=f"attributes.`run_name`='{run_name}'",
                output_format="list",
            )

            if current_runs:
                run_id = current_runs[0].info.run_id
                return mlflow.start_run(run_id=run_id, run_name=run_name)
            else:
                tags["dagster.run_id"] = get_run_id(context)
                tags["dagster.asset_name"] = get_asset_key(context)

                return mlflow.start_run(run_name=run_name, tags=tags)

        return active_run