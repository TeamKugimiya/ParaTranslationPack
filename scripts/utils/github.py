"""
Misc Utils for GitHub
"""
import os
import sys
from pathlib import Path
from loguru import logger


def github_write_step_output(step_output_name: str, data: str):
    """
    Write step output to GITHUB_OUTPUT environment.

    Args:
        step_output_name (str):
            Step output name.
        data (str):
            Step output data.
    """
    github_step_output_env = os.environ.get("GITHUB_OUTPUT")

    if github_step_output_env is None:
        logger.error("GITHUB_OUTPUT environment variable is not set!")
        sys.exit(1)

    github_step_output_path = Path(github_step_output_env)

    try:
        with github_step_output_path.open("a") as output_file:
            output_file.write(f"{step_output_name}={data}")
            output_file.close()
    except Exception as e:
        logger.error(f"Failed to write to GITHUB_OUTPUT: {e}")
        sys.exit(1)
