from typing import Literal

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


def canonical_lakefs_uri_for_input(
    context: dg.AssetExecutionContext,
    input_name: str,
    protocol: Literal["lakefs", "s3"] = "lakefs",
) -> str:
    """Return the canonical lakeFS URI for a given input asset (must be managed by a lakeFS I/O manager).

    Parameters
    ----------
    context : dg.AssetExecutionContext
        Dagster asset execution context, providing information about the current run.
    input_name : str
        Name of the input asset
    protocol : Literal["lakefs", "s3"], optional, default "lakefs"
        Protocol to use in the URI (lakefs or S3)

    Returns
    -------
    str
        Canonical lakeFS URI
    """
    ev = context.instance.get_latest_materialization_event(
        context.asset_key_for_input(input_name)
    )
    metadata = ev.asset_materialization.metadata
    if "canonical_uri" not in metadata:
        raise ValueError("No canonical URI found in metadata")

    uri = metadata.get("canonical_uri").value
    if protocol == "s3":
        uri = uri.replace("lakefs://", "s3://")
    return uri
