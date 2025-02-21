import json
import tomllib
import pytz
from pathlib import Path
from loguru import logger
from datetime import datetime
from jsonschema import validate, ValidationError


def calculate_percentage(part, whole) -> float:
    """
    Calculate the percentage of `part` with respect to `whole`.

    Args:
        part (int): The part value.
        whole (int): The whole value.

    Returns:
        float: The percentage value.
    """
    if whole == 0:
        logger.error("The whole value cannot be zero.")
    return round((part / whole) * 100, 2)


def load_jsondata(path: str) -> dict:
    """
    Load json data from file

    Args:
        path (str):
            Path to the json file

    Returns:
        dict:
            The data from the json file
    """
    path = Path(path)
    try:
        with path.open("rb") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    return {}


def load_tomldata(path: Path) -> dict:
    """
    Load toml data from file

    Args:
        path (str):
            Path to the toml file

    Returns:
        dict:
            The data from the toml file
    """
    path = Path(path)
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
            return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except tomllib.TOMLDecodeError as e:
        logger.error(f"Error decoding TOML: {e}")
    return {}


def validate_json_schema(data: dict, schema: dict) -> bool:
    """
    Validate JSON data against a schema.

    Args:
        data (dict): The JSON data to validate.
        schema (dict): The JSON schema to validate against.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        logger.error(f"JSON validation error: {e}")
        return False


def convert_epoch(timestamp: str) -> int:
    """Convert ISO timestamp to epoch time.

    Args:
        timestamp (str):
            Timestamp.

    Returns:
        int:
            Epoch time.
    """
    iso_timestamp = timestamp
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    epoch_time = dt.timestamp()
    return epoch_time


def copy_file(src: str, dest: str) -> bool:
    """
    Copy file from source to destination.

    Args:
        src (str): Source file path.
        dest (str): Destination file path.

    Returns:
        bool: True if the file is copied successfully, False otherwise.
    """
    src = Path(src)
    dest = Path(dest)
    try:
        dest.write_bytes(src.read_bytes())
        return True
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"Error copying file: {e}")
    return False


def current_date() -> str:
    """Get current date.

    Returns:
        str:
            Current date.
    """
    tz = pytz.timezone("Asia/Taipei")
    return datetime.now(tz).strftime("%Y/%m/%d")


def current_time() -> str:
    """Get current time.

    Returns:
        str:
            Current time.
    """
    tz = pytz.timezone("Asia/Taipei")
    return datetime.now(tz).strftime("%H:%M:%S")


def current_dtime() -> str:
    """Get current date and time.

    Returns:
        str:
            Current date and time.
    """
    tz = pytz.timezone("Asia/Taipei")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
