"""
Get ParaTranz artifact id data and write it to cache file.
"""
import os
from pathlib import Path
from loguru import logger
from paratranz_py import ParaTranz


def paratranz_write_cache(
        artifact_data: dict, cache_path: Path, cache_fname: str
) -> bool:
    """
    Write ParaTranz artifact id data to cache file.

    Args:
        artifact_data (dict):
            ParaTranz artifact data.
        cache_path (Path):
            Cache folder path.
        cache_fname (str):
            Cache file name.
    """
    cache_path = Path(cache_path)
    data_value = str(artifact_data["id"])
    cache_file_path = cache_path.joinpath(cache_fname)

    if not cache_path.exists():
        cache_path.mkdir()

    if not cache_file_path.exists():
        logger.info("Cache file is missing, create one.")
        cache_file_path.write_text(data_value)

    if cache_file_path.exists():
        cache_value = cache_file_path.read_text()
        if cache_value == data_value:
            logger.info("Cache file is same as data!")
        else:
            logger.info("Cache file is not same as data, overwrite!")
            cache_file_path.write_text(data_value)


def run():
    cache_folder = ".cache"
    cache_file = "paratranz_id_cache.txt"
    project_id = os.getenv("PARATRANZ_PROJECT_ID")
    api_token = os.getenv("PARATRANZ_API_TOKEN")
    para = ParaTranz(
        api_token=api_token
    )

    artifact_data = para.artifacts.get_artifacts_info(project_id)
    paratranz_write_cache(artifact_data, cache_folder, cache_file)


if __name__ == "__main__":
    run()
