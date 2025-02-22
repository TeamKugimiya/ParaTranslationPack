import os
from datetime import datetime
from loguru import logger
from paratranz_py import ParaTranz
from scripts.utils import calculate_percentage, current_date, current_dtime, current_r2 # noqa
from discord_webhook import DiscordWebhook, DiscordEmbed

para = ParaTranz(os.getenv("PARATRANZ_TOKEN"))
mr_url = "https://modrinth.com/resourcepack/paratranslationpack"
r2_url = "https://teamkugimiya-r2.efina.eu.org/paratranslationpack/"

data = para.artifacts.get_artifacts_info("9900")

desc = f""":pencil: 翻譯追蹤
- 總詞條數：`{data["total"]}`
- 已翻譯條數：`{data["translated"]}`
- 有疑問條數：`{data["disputed"]}`
- 翻譯完成度：**{calculate_percentage(data["translated"], data["total"])}%**
:construction: 下載翻譯包
> 測試建構版
- 發布號 {current_date()}
- 建構時間 {current_dtime()}
- [下載測試版 1.18]({r2_url}{current_r2()}/ParaTranslationPack-1.18.x.zip)
- [下載測試版 1.19]({r2_url}{current_r2()}/ParaTranslationPack-1.19.x.zip)
- [下載測試版 1.20]({r2_url}{current_r2()}/ParaTranslationPack-1.20.x.zip)
- [下載測試版 1.21]({r2_url}{current_r2()}/ParaTranslationPack-1.21.x.zip)
> 發布版
- Modrinth - [ParaTranslationPack]({mr_url})
"""

webhook = DiscordWebhook(
    url=os.getenv("DC_WEBHOOK_URL"),
    id=os.getenv("DC_WEBHOOK_ID")
)

embed = DiscordEmbed(
    title="ParaTranslationPack",
    description=desc,
    color="2f3136"
)
embed.set_thumbnail(url="https://cdn.modrinth.com/data/7DO0XWSK/26578cea26e7743d4377ddbc4f4ad69072e3147c_96.webp") # noqa
embed.set_timestamp(datetime.now().timestamp())

webhook.add_embed(embed)


def run():
    resp = webhook.edit()

    if int(resp.status_code) == 200:
        logger.success("Webhook sucess updated.")
    else:
        logger.error(f"Webhook update failed: {resp.status_code}")


if __name__ == "__main__":
    run()
