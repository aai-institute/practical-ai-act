import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile


@dataclass(frozen=True)
class ContainerBuildResult:
    success: bool
    build_logs: str | None = None
    image_name: str | None = None
    image_digest: str | None = None


def build_container_image(
    build_context: Path,
    tags: list[str],
    network: str | None = None,
    build_args: dict[str, str] | None = None,
    dockerfile_path: Path | None = None,
) -> ContainerBuildResult:
    """Builds a Docker container image using buildx from the given build context.

    Parameters
    ----------
    build_context : Path
        Path to the directory containing the Dockerfile.
    tags : list[str]
        List of tags to apply to the built image.
    network : str, optional
        Network mode to use for the build. Defaults to None (i.e., no explicit network mode).
    build_args : dict[str, str], optional
        Dictionary of build arguments to pass to the Docker build process. Defaults to None.
    dockerfile_path : Path, optional
        Path to the Dockerfile to use for the build. Defaults to None (i.e., `Dockerfile`).

    Returns
    -------
    ContainerBuildResult
        The results of the image build
    """

    if not build_context.is_dir():
        raise ValueError(f"Build context {build_context} is not a directory")

    with NamedTemporaryFile(suffix=".json", delete_on_close=False) as metadata_file:
        tags_args = [f"-t={tag}" for tag in tags]
        cmd = [
            "docker",
            "buildx",
            "build",
            *tags_args,
            "--metadata-file",
            metadata_file.name,
            str(build_context),
        ]

        if dockerfile_path is not None:
            cmd.extend(["--file", str(dockerfile_path.relative_to(build_context))])

        if network:
            cmd.extend(["--network", network])

        if build_args:
            cmd.extend([
                f"--build-arg={key}={value}" for key, value in build_args.items()
            ])

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, encoding="utf-8")
            build_logs = None
            success = True
        except subprocess.CalledProcessError as e:
            success = False
            print(f"Error building container image: {e}")
            build_logs = e.stdout

        # Extract image digest from metadata file
        metadata = {}
        metadata_file.close()
        metadata_str = Path(metadata_file.name).read_text()
        if metadata_str:
            metadata = json.loads(metadata_str)
            try:
                # Extract build logs from buildx history
                buildx_build_id = metadata["buildx.build.ref"].split("/")[-1]
                cmd = [
                    "docker",
                    "buildx",
                    "history",
                    "logs",
                    buildx_build_id,
                ]
                build_logs = subprocess.check_output(
                    cmd, stderr=subprocess.STDOUT, encoding="utf-8"
                )
            except subprocess.CalledProcessError as e:
                build_logs = e.stdout

        return ContainerBuildResult(
            success=success,
            build_logs=build_logs,
            image_name=metadata.get("image.name"),
            image_digest=metadata.get("containerimage.digest"),
        )
