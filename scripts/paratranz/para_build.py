import os
import json
from pathlib import Path
from loguru import logger
from paratranz_py import ParaTranz
from scripts.utils import (
    validate_json_schema,
    load_jsondata,
    convert_epoch,
    current_date,
    copy_file,
    remove_dir,
)


PATH_WORKDIR = Path("workdir")
PATH_ARTIFACT = PATH_WORKDIR.joinpath("artifact_data")
PATH_ASSETS = PATH_WORKDIR.joinpath("assets")
LANG_SCHEMA = load_jsondata("configs/mc-schema.json")


def download_artifact(para: ParaTranz, project_id: str):
    """
    Download artifact from ParaTranz.

    Args:
        para (ParaTranz):
            ParaTranz instance.
        project_id (str):
            ParaTranz project ID.
    """
    para.artifacts.download_artifacts(
        project_id=project_id, extract_path=PATH_WORKDIR.joinpath("artifact_data")
    )


def modify_file_date(para: ParaTranz, project_id: int):
    """
    Modify file date based on ParaTranz artifact data.

    Args:
        para (ParaTranz):
            ParaTranz instance.
    """
    artifact_data = para.files.get_files(project_id)

    for file in PATH_ARTIFACT.glob("**/*.json"):
        multiversion_name = str(Path(*file.parts[3:]))

        for artifact in artifact_data:
            if multiversion_name in artifact["name"]:
                artifact_time = artifact["modifiedAt"]
                epoch_time = convert_epoch(artifact_time)
                old_a_time = os.path.getatime(file)
                old_m_time = os.path.getmtime(file)
                os.utime(file, (epoch_time, epoch_time))
                new_a_time = os.path.getatime(file)
                new_m_time = os.path.getmtime(file)

                logger.info(
                    "\n"
                    f"Modified file: {multiversion_name}\n"
                    f"- Last Modify Time: {artifact_time}\n"
                    f"- Modify Time {old_m_time} -> {new_m_time}\n"
                    f"- Access Time {old_a_time} -> {new_a_time}"
                )
                break
        else:
            logger.error(f"File not found: {multiversion_name}")


def validate_mc_lang_data(path) -> bool:
    """
    Validate lang data.

    Args:
        path (str):
            Path to lang data.

    Returns:
        bool:
            True if validation is successful.
    """
    return validate_json_schema(load_jsondata(path), LANG_SCHEMA)


def format_resourcepack():
    """
    Format resourcepack data.
    """
    if not PATH_ASSETS.exists():
        PATH_ASSETS.mkdir()
    for file_path in PATH_ARTIFACT.glob("**/*.json"):
        mod_id = file_path.name.removesuffix(".json")
        if validate_mc_lang_data(file_path):
            if not load_jsondata(file_path):
                logger.warning(f"Empty lang data: {mod_id}")
                continue
            assets_mod_id = PATH_ASSETS.joinpath(f"{mod_id}/lang/zh_tw.json")
            assets_mod_id.parents[0].mkdir(parents=True)
            copy_file(file_path, assets_mod_id)
            logger.success("Moved to assets: " + mod_id)
        else:
            logger.error(f"Invalid lang data: {mod_id}")


def generate_pack_format(
    pack_format: int, mc_supported_format_min: int, mc_supported_format_max: int
):
    """
    Generate pack format.
    """
    format_file = PATH_WORKDIR.joinpath("pack.mcmeta")
    date = current_date()
    pack_mcmeta = {
        "pack": {
            "pack_format": int(pack_format),
            "supported_formats": {
                "min_inclusive": int(mc_supported_format_min),
                "max_inclusive": int(mc_supported_format_max),
            },
            "description": [
                f"§fPara 翻譯包｜§b{date}\n",
                "§3感謝所有參與專案的貢獻者！",
            ],
        }
    }
    json_data = json.dumps(pack_mcmeta, ensure_ascii=False)
    format_file.write_text(json_data)


def copy_files():
    """
    Copy nessessory files
    """
    icon_path = Path("assets/pack.png")
    license_path = Path("assets/LICENSE")
    copy_file(icon_path, PATH_WORKDIR.joinpath("pack.png"))
    copy_file(license_path, PATH_WORKDIR.joinpath("LICENSE"))


def chore():
    """
    Cleanup folder
    """
    remove_dir(PATH_ARTIFACT)


def fix_new_line():
    """
    Temporary fix for new line.
    Replace \\n to \n
    """
    for file in PATH_ARTIFACT.glob("**/*.json"):
        data = file.read_text()
        if "\\n" in data:
            new_data = data.replace("\\\\n", "\\n")
            if new_data != data:
                file.write_text(new_data)
                logger.success(f"Fixed new line: {file.name}")


def run():
    para_token = os.getenv("PARATRANZ_TOKEN")
    para_project_id = 9900
    paratranz = ParaTranz(para_token)

    pack_format = os.getenv("MC_PACK_FORMAT")
    mc_supported_format_min = os.getenv("MC_SUPPORTED_FORMAT_MIN")
    mc_supported_format_max = os.getenv("MC_SUPPORTED_FORMAT_MAX")

    download_artifact(paratranz, para_project_id)
    fix_new_line()
    modify_file_date(paratranz, para_project_id)
    format_resourcepack()
    generate_pack_format(pack_format, mc_supported_format_min, mc_supported_format_max)
    copy_files()
    chore()


if __name__ == "__main__":
    run()
