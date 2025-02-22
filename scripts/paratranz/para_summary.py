import os
import pytz
from datetime import datetime
from loguru import logger
from paratranz_py import ParaTranz
from scripts.utils import calculate_percentage, github_write_step_output


def timestamp_format(timestamp: str):
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    tz_taipei = pytz.timezone("Asia/Taipei")
    dt_taipei = dt.replace(tzinfo=pytz.utc).astimezone(tz_taipei)
    formatted_date = dt_taipei.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_date


def paratranz_modrinth_generate_summary(artifact_data: dict):
    logger.info("Generate modrinth summary...")

    date_time = timestamp_format(artifact_data['createdAt'])
    completion_percent = calculate_percentage(artifact_data['translated'], artifact_data['total']) # noqa

    summary = f"""## 🌏 翻譯資訊
- Para 建構時間：`{date_time}`
- 總詞條數：`{artifact_data['total']}`
- 已翻譯條數：`{artifact_data['translated']}`
- 有疑問條數：`{artifact_data['disputed']}`
- 翻譯完成度：**{completion_percent:.2f}%**
"""
    logger.info("Generated modrinth summary:")
    logger.info(summary)
    return summary


def run():
    api_token = os.getenv("PARATRANZ_TOKEN")
    project_id = 9900
    para = ParaTranz(
        api_token=api_token
    )
    artifact_data = para.artifacts.get_artifacts_info(project_id)
    summary_data = paratranz_modrinth_generate_summary(artifact_data)
    github_write_step_output("summary", summary_data)


if __name__ == "__main__":
    run()
