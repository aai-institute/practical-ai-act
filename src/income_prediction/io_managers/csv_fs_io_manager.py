"""Custom IO manager for saving and loading DataFrames as CSV files."""

import os

import pandas as pd
from dagster import ConfigurableIOManager, InputContext, OutputContext


class CSVFSIOManager(ConfigurableIOManager):
    """Custom IO manager for saving and loading DataFrames as CSV files.

    Attributes
    ----------
    base_dir : str
        The directory for saving and loading CSV files.
    extension : str, default ".csv"
        The file extension for the output files.
    """

    base_dir: str
    extension: str = ".csv"

    def _get_path(self, context: InputContext | OutputContext) -> str:
        """Generates a file path by combining the base directory, asset key path, and file extension.

        Parameters
        ----------
        context : Union[InputContext, OutputContext]
            The Dagster context (input or output) that provides information about the asset.

        Returns
        -------
        str
            The file path for the asset.
        """
        return os.path.join(self.base_dir, *context.asset_key.path) + self.extension

    def handle_output(self, context: OutputContext, obj: pd.DataFrame) -> None:
        """Saves the DataFrame to a CSV file.

        The file path is based on the specified base directory and the asset key path. If the directory does not yet
        exist, it is created.

        Parameters
        ----------
        context : OutputContext
            The Dagster output context, which provides information about the asset and is used for logging.
        obj : pd.DataFrame
            The DataFrame to be saved as a CSV file.

        """
        path = self._get_path(context)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        context.log.debug(f"Writing file at: {path}")
        obj.to_csv(path)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Loads a DataFrame from a CSV file.

        The file path is based on the specified base directory and asset key path.

        Parameters
        ----------
        context : InputContext
            The Dagster input context, which provides information about the asset and is used for logging.

        Returns
        -------
        pd.DataFrame
            A DataFrame loaded from the specified CSV file.
        """
        path = self._get_path(context)

        context.log.debug(f"Reading file from: {path}")
        return pd.read_csv(path)
