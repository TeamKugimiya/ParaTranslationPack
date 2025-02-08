import os
import json
import tomllib
from pathlib import Path
from loguru import logger

def load_jsondata(path: Path) -> dict:
    """
    Load json data from file
    
    Parameters:
    - path (Path): Path to the json file

    Returns:
    - dict: The data from the json file
    """
    try:
        with open(path, "rb") as f:
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
    
    Parameters:
    - path (Path): Path to the toml file

    Returns:
    - dict: The data from the toml file
    """
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
            return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except tomllib.TOMLDecodeError as e:
        logger.error(f"Error decoding TOML: {e}")
    return {}

def github_write_step_output(step_output_name: str, data: str):
    """
    Write step output to GITHUB_OUTPUT
    
    Parameters:
    - step_output_name (str): Name of the step output
    - data (str): Data to write
    """
    github_step_output_env = os.environ.get("GITHUB_OUTPUT")

    if github_step_output_env is None:
        logger.error("GITHUB_OUTPUT environment variable is not set!")

    github_step_output_path = Path(github_step_output_env)

    try:
        with github_step_output_path.open("a") as output_file:
            output_file.write(f"{step_output_name}={data}")
            output_file.close()
    except Exception as e:
        logger.error(f"Failed to write to GITHUB_OUTPUT: {e}")
