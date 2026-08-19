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
本庫只保存呼叫 reusable workflows 的薄型 CI caller；同步與建構實作仍由外部工具 release 提供。

預定同步循環如下：模組原文更新先進 source PR；合併後由 `paratranz-tool` 更新 ParaTranz，
新模組會自動建立遠端檔案並回寫 identity manifest。譯文同步每小時先做輕量更新偵測，只有
ParaTranz 有新譯文或尚未套用的 artifact 時才下載、驗證、建構並建立 `zh_tw.json` PR。
Repository 移除模組時只產生 retained warning，不會自動刪除遠端檔案或既有翻譯。

目前已準備 source sync 與每小時 translation pull caller。Toolkit version 與 ModsTranslationPack
相同，預設不傳版本並安裝 GitHub latest release，同時驗證 `SHA512SUMS`；需要重現時才固定 tag。
本階段尚未加入自動發布。

## 翻譯資料結構

```text
Translation/<content_id>/metadata.json
Translation/<content_id>/<latest_tier>/en_us.json
Translation/<content_id>/<latest_tier>/zh_tw.json
```

每個模組只保存一個實際最新版 tier，不將同一份翻譯複製到所有 Minecraft 版本。

## 授權

本專案採用 [CC BY-NC-ND 4.0](LICENSE)。第三方內容仍受其原始授權條款約束。
