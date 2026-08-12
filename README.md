![ParaTranslationPack-Banner](.github/assets/banner.png)

# Para 翻譯包

由 ParaTranz 社群協作維護的 Minecraft 模組繁體中文資源包。本 repository 是翻譯資料來源，
目前收錄 157 個模組；翻譯請前往 [ParaTranz 專案](https://paratranz.cn/projects/9900) 貢獻。

## Repository 內容

- `Translation/**`：各模組最新版英文原文、繁中譯文與 metadata。
- `config/**`：版本群組、資源包圖示、ParaTranz project 設定及 `mod_id → file_id` identity manifest。
- `docs/project.md`：本專案固定設定與資料邊界。
- `docs/migration.md`：舊 ParaTranz 結構轉移紀錄與剩餘上線閘門。

建構、ParaTranz API client、同步與發布實作不在本庫長期維護，會由固定版本的
[`translation-toolkit`](https://github.com/TeamKugimiya/translation-toolkit)、
[`paratranz-toolkit`](https://github.com/TeamKugimiya/paratranz-toolkit) 與 reusable workflows 提供。
正式自動化啟用時，本庫只會加入呼叫 reusable workflows 的薄型 CI caller。

## 翻譯資料結構

```text
Translation/<content_id>/metadata.json
Translation/<content_id>/<latest_tier>/en_us.json
Translation/<content_id>/<latest_tier>/zh_tw.json
```

每個模組只保存一個實際最新版 tier，不將同一份翻譯複製到所有 Minecraft 版本。

## 授權

本專案採用 [CC BY-NC-ND 4.0](LICENSE)。第三方內容仍受其原始授權條款約束。
