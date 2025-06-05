import dagster as dg
import lakefs_spec.util
import pandas as pd
from dagster import InputContext, OutputContext
from upath import UPath


class LakeFSParquetIOManager(dg.UPathIOManager):
    """IO Manager for reading and writing Parquet files in a LakeFS repository.

    Note that the `fastparquet` engine is used for reading and writing Parquet files
    in order to preserve Pandas dtypes like `category`.
    """

    extension = ".parquet"

    @staticmethod
    def _canonical_uri_for_output(context: InputContext) -> str | None:
        # TODO: This only works for non-partitioned assets
        # Once https://github.com/dagster-io/dagster/issues/20094 is resolved, we can
        # directly access the output metadata, without having to go through the materialization
        # events.
        asset_key = context.asset_key
        mat_event = context.instance.get_latest_materialization_event(asset_key)
        meta = mat_event.dagster_event.event_specific_data.materialization.metadata
        return str(uri.value) if (uri := meta.get("canonical_uri")) else None

    def _get_path(self, context: dg.InputContext | dg.OutputContext) -> UPath:
        if isinstance(context, dg.InputContext):
            # Read the canonical URI from the metadata of the upstream asset materialization
            # Reading from the raw path could cause a race condition if the repository (or
            # rather the branch HEAD referred to in the `base_path`) has changed since the
            # asset was materialized.
            canonical_uri = self._canonical_uri_for_output(context)
            if canonical_uri is None:
                raise RuntimeError("No canonical path found in metadata")
            return UPath(
                canonical_uri,
                **self._base_path.storage_options,
            )
        else:
            return super()._get_path(context)

    def load_from_path(self, context: InputContext, path: "UPath") -> pd.DataFrame:
        # Note: this will read from the immutable commit ref, not the branch HEAD,
        # which could lead to inconsistent data if the branch has been updated since
        # the asset was materialized.
        # See also the implementation of `_get_path`.
        return pd.read_parquet(
            path, engine="fastparquet", storage_options=dict(path.storage_options)
        )

    def dump_to_path(
        self, context: OutputContext, obj: pd.DataFrame, path: "UPath"
    ) -> None:
        repo, ref, resource = lakefs_spec.util.parse(path.path)
        with path.fs.transaction(
            repository=repo,
            base_branch=ref,
        ) as tx:
            self.make_directory(path)

            # Need to add the file to the transaction branch, which gets then merged into the target branch
            ephemeral_path = f"lakefs://{repo}/{tx.branch.id}/{resource}"
            obj.to_parquet(
                ephemeral_path,
                engine="fastparquet",
                storage_options=dict(path.storage_options),
            )

            asset_id_str = "/".join(context.get_asset_identifier())
            commit_ref = tx.commit(
                message=f"Add data from {asset_id_str!r}",
                metadata={
                    "dagster.run_id": str(context.run_id),
                    "dagster.asset_identifier": asset_id_str,
                },
            )

            # Record commit ref with hash in asset metadata
            context.add_output_metadata({
                "commit_id": commit_ref.id,
                "canonical_uri": f"lakefs://{repo}/{commit_ref.id}/{resource}",
            })
