import dagster as dg
import lakefs_spec.util
import pandas as pd
from dagster import InputContext, OutputContext
from upath import UPath


class LakeFSParquetIOManager(dg.UPathIOManager):
    extension = ".parquet"

    def load_from_path(self, context: InputContext, path: "UPath") -> pd.DataFrame:
        return pd.read_parquet(path, storage_options=dict(path.storage_options))

    def dump_to_path(
        self, context: OutputContext, obj: pd.DataFrame, path: "UPath"
    ) -> None:
        repo, ref, resource = lakefs_spec.util.parse(path.path)
        with path.fs.transaction(
            repository=repo,
            base_branch=ref,
        ) as tx:
            path.mkdir(parents=True, exist_ok=True)

            # Need to add the file to the transaction branch, which gets then merged into the target branch
            ephemeral_path = f"lakefs://{repo}/{tx.branch.id}/{resource}"
            obj.to_parquet(ephemeral_path, storage_options=dict(path.storage_options))

            commit_ref = tx.commit(
                message=f"Add data from {context.asset_key.path}",
                metadata={
                    "dagster.run_id": str(context.run_id),
                    "dagster.asset_key": str(context.asset_key.path),
                },
            )

            # Record commit ref with hash in asset metadata
            context.add_output_metadata({
                "commit_id": commit_ref.id,
                "canonical_uri": f"lakefs://{repo}/{commit_ref.id}/{resource}",
            })
