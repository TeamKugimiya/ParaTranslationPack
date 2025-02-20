import json
import tomllib
from pathlib import Path
from loguru import logger
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
