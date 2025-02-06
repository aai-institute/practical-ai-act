import dagster as dg

SHORT_RUN_ID_LENGTH = 8
"""Number of characters to include in the shortened version of the run ID."""


def extract_run_id(context: dg.AssetExecutionContext, short: bool = False) -> str:
    """Retrieves the run ID from the Dagster execution context.

    If `short` is True, returns only the first `SHORT_RUN_ID_LENGTH` characters.

    Parameters
    ----------
    context : dg.AssetExecutionContext
        Dagster asset execution context, providing information about the current run.
    short : bool, optional, default False
        If True, returns a shortened version of the run ID.

    Returns
    -------
    str
        Full or shortened run ID for the current execution.
    """
    run_id = context.run.run_id
    return run_id if not short else run_id[:SHORT_RUN_ID_LENGTH]
