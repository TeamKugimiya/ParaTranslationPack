"""
Get Modrinth release version to check is it duplicate or not.
"""
import requests
import pytz
from scripts.utils import github_write_step_output
from loguru import logger
from datetime import datetime


def get_modrinth_latest_publish_date() -> str:
    """
    Get Modrinth latest release publish date.

    Returns:
        str:
            Modrinth latest release publish date.
    """
    url = "https://api.modrinth.com/v2/project/paratranslationpack/version"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[0]["date_published"].split("T")[0]


def get_current_date() -> str:
    """
    Get current date.

    Returns:
        str:
            Current date.
    """
    tz = pytz.timezone("Asia/Taipei")
    return datetime.now(tz).date()

def run():
    modrinth_latest_release_date = get_modrinth_latest_publish_date()
    current_date = get_current_date()
    logger.debug("Modrinth: {} | Current: {}", modrinth_latest_release_date, current_date) # noqa
    is_same_date = modrinth_latest_release_date == current_date
    logger.info(f"Modrinth latest release date is {'same' if is_same_date else 'not same'} as current date!") # noqa
    github_write_step_output("is_same_date", str(is_same_date).lower())


if __name__ == "__main__":
    run()
