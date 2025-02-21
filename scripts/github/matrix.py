from pathlib import Path
from loguru import logger
from scripts.utils import load_tomldata, github_write_step_output

CONFIG_PATH = Path("configs/versions.toml")


def matrix_generate(version_data: dict) -> dict:
    matrix_versions = {
        "include": [
            {
                "mc_version": v.get("mc_version"),
                "mc_pack_format": v.get("mc_pack_format"),
                "mc_supported_formats_min": v.get("mc_supported_formats_min"),
                "mc_supported_formats_max": v.get("mc_supported_formats_max"),
                "modrinth_version": v.get("modrinth_version"),
                "directory_path": v.get("directory_path")
            }
            for v in version_data.get("versions", [])
        ]
    }
    logger.debug(matrix_versions)
    return matrix_versions


def run():
    config_data = load_tomldata(CONFIG_PATH)
    matrix_json = matrix_generate(config_data)
    github_write_step_output("matrix_data", matrix_json)


if __name__ == "__main__":
    run()
