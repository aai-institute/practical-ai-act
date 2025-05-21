import logging
import os

# Must set before importing Dagster definitions, since the env var is used to determine the environment
os.environ["DAGSTER_IS_DEV_CLI"] = "1"

from income_prediction import definitions
from income_prediction.jobs import e2e_pipeline_job

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Trigger Dagster e2e training pipeline
    definitions.get_job_def(e2e_pipeline_job.name).execute_in_process()
