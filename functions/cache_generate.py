"""
Get ParaTranz artifact id data and write it to cache file.
"""
from pathlib import Path
from loguru import logger

def paratranz_write_cache(artifact_data: dict, cache_path: Path, cache_fname: str) -> bool:
    """
    Write ParaTranz artifact id data to cache file.
    
    Parameters:
    - artifact_data: dict - ParaTranz artifact data.
    - cache_path: Path - Cache file path.
    - cache_fname: str - Cache file name.
    
    Returns:
    - bool: True if cache file is same as data, False if cache file is not same as data.
    """
    cache_path = Path(cache_path)
    data_value = str(artifact_data["id"])
    cache_file_path = cache_path.joinpath(cache_fname)

    if not cache_path.exists():
        cache_path.mkdir()

    if not cache_file_path.exists():
        logger.info("Cache file is missing, create one.")
        cache_file_path.write_text(data_value)
        return False

    if cache_file_path.exists():
        cache_value = cache_file_path.read_text()
        if cache_value == data_value:
            logger.info("Cache file is same as data!")
            return True
        else:
            logger.info("Cache file is not same as data, overwrite!")
            cache_file_path.write_text(data_value)
            return False
