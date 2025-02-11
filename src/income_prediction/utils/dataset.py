import urllib
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


def download_file(url: str, destination: Path) -> None:
    """Downloads a file from the given url and saves it to the specified destination.

    Parameters
    ----------
    url : str
        URL to download the file from.
    destination : Path
        The local path where the downloaded file should be saved.

    Raises
    ------
    ValueError
        If the file download fails.
    """
    try:
        urllib.request.urlretrieve(url, destination)
    except urllib.error.URLError as e:
        raise ValueError(f"Failed to download data from {url}: {e}")


def extract_file_from_zip(zip_path: Path, expected_file: str, extract_to: Path) -> None:
    """Extracts a specific file from a ZIP archive.

    Parameters
    ----------
    zip_path : Path
        Path to the ZIP archive.
    expected_file : str
        Name of the file to extract.
    extract_to : str
        Directory where the extracted file should be saved.

    Raises
    ------
    ValueError
        If the ZIP archive is invalid or does not contain the expected file.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            if expected_file not in zip_ref.namelist():
                raise ValueError(f"File '{expected_file}' not found in ZIP archive.")

            zip_ref.extract(expected_file, extract_to)
    except zipfile.BadZipFile as e:
        raise ValueError(f"Invalid ZIP archive: {e}")
