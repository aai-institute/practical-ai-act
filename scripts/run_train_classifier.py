import logging
import time

import dagster as dg
from dagster_graphql import DagsterGraphQLClient

log = logging.getLogger(__name__)

_TERMINAL_STATES = {
    dg.DagsterRunStatus.SUCCESS,
    dg.DagsterRunStatus.FAILURE,
    dg.DagsterRunStatus.CANCELED,
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # The GraphQL client logger is quite verbose
    logging.getLogger("gql").setLevel(logging.WARNING)

    client = DagsterGraphQLClient(
        hostname="localhost",
        port_number=3000,
        use_https=False,
    )
    run_id = client.submit_job_execution(
        job_name="e2e_pipeline_job",
        tags={"source": "cli"},
    )
    log.info(f"Dagster run ID: {run_id}")

    # Wait for the job to finish, allowing for a graceful exit on Ctrl+C
    try:
        while (status := client.get_run_status(run_id)) not in _TERMINAL_STATES:
            log.info(f"Run status: {status.value}, waiting for completion...")
            time.sleep(5)
        log.info(f"Run finished with status: {status.value}")
    except KeyboardInterrupt:
        log.info("Job execution interrupted by user, terminating Dagster run.")
        client.terminate_run(run_id)
