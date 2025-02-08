import requests
from pathlib import Path
from loguru import logger
from pooch import retrieve, HTTPDownloader, Unzip

class ParaTranz:
    def __init__(self, project_id: int, api_token: str, api_url: str="https://paratranz.cn/api"):
        """
        Initialize the ParaTranz class.

        Parameters:
        project_id (int): The project ID.
        api_token (str): The API token.
        api_url (str): The API URL (default: "https://paratranz.cn/api").
        """
        self._project_id = project_id
        self.api_token = api_token
        self._api_url = api_url
        self.headers = {
            "Authorization": f"{api_token}",
            "User-Agent": "Paratranz Script | Made by @xMikux"
        }

    ### Projects
    def get_project(self) -> dict:
        """
        Get project information.

        Returns:
        dict: The project information.
        """
        url = f"{self._api_url}/projects/{self._project_id}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get project information: {str(e)}")
            return {"error": str(e)}

    ### Artifacts

    def get_artifacts(self) -> dict:
        """
        Get project artifacts information.

        Returns:
        dict: The project artifacts information.
        """
        url = f"{self._api_url}/projects/{self._project_id}/artifacts"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get artifacts information: {str(e)}")
            return {"error": str(e)}

    def make_artifact(self) -> dict:
        """
        Trigger a new artifact build.

        Returns:
        dict: The response from the server.
        """
        url = f"{self._api_url}/projects/{self._project_id}/artifacts"
        try:
            response = requests.post(url, headers=self.headers)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to trigger artifact build: {str(e)}")
            return {"error": str(e)}

    def download_artifacts(self, path: Path=None, artifacts_name: str="artifact.zip", extract_path: Path=None):
        """
        Download project artifacts.

        Parameters:
        path (Path): Path to save the artifact file (if None, it will save on pooch cache).
        artifacts_name (str): Name of the artifact file.
        extract_path (Path): Path to extract the artifact file.
        """
        url = f"{self._api_url}/projects/{self._project_id}/artifacts/download"

        if extract_path is not None:
            extract_path = Path(extract_path)
            extract_dir_path = Unzip(extract_dir=extract_path.absolute())
        else:
            extract_dir_path = None

        try:
            retrieve(
                url,
                path=path,
                fname=artifacts_name,
                known_hash=None,
                processor=extract_dir_path,
                downloader=HTTPDownloader(headers=self.headers)
            )
        except Exception as e:
            logger.error(f"Download Failed! Error: {str(e)}")

