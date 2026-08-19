# ParaTranslationPack 專案設定

本文件只記錄 ParaTranslationPack 特有的資料、政策與共享工具版本邊界。CLI、API、安全限制、
同步演算法與 workflow inputs 的完整契約應維護在其實作 repository，不在本庫複製。

## Repository 定位

本 repository 比照 ModsTranslationPack，正式分支長期只保存：

- `Translation/**` 的 `metadata.json`、`en_us.json` 與 `zh_tw.json`；
- `config/**` 的版本、圖示、來源例外與 ParaTranz identity 設定；
- README、LICENSE 與 project-specific 文件；
- 呼叫集中式 reusable workflow 的薄型 GitHub Actions caller。

API client、同步器、格式轉換器、建構器、發布程式、測試 fixture 與遷移來源封存不屬於長期
repository 內容。舊程式與 workflow 已退出版本控制；切換期所需的本機副本、遷移工具、測試與
稽核報告由 `.gitignore` 排除，待新流程穩定後移至外部封存或刪除。

## ParaTranz profile

| 欄位 | 值 |
| --- | --- |
| Project ID | `9900` |
| Adapter | `translation-pack-v1` |
| Project config | `config/paratranz.json` schema 1 |
| Identity manifest | `config/paratranz-files.json` schema 2 |
| Pull state | `config/paratranz-sync-state.json` schema 1（首次完整 pull 後建立） |
| Current files | 157 |
| Remote path | `Translation/{content_id}/{tier}/{mod_id}.json` |
| Artifact prefix | `utf8` |
| Token | 僅由 `PARATRANZ_TOKEN` secret 注入 |

Manifest 只保存 immutable `mod_id → file_id`，不保存 `content_id`、tier、remote path 或遷移
狀態。Desired path 每次由 current repository 計算，stable remote identity 永遠是 `file_id`。
正式契約見 [paratranz-toolkit SPEC](https://github.com/TeamKugimiya/paratranz-toolkit/blob/main/docs/spec.md)。

## Translation profile

- 每個 current 模組只保留一個實際最新版 tier，例如 `1.21`、`26.1` 或 `26.2`。
- `versions` 使用 `<=@latest`，由資源包版本群組決定向下沿用範圍。
- 模組來源搜尋以 CurseForge 優先，Modrinth 或明確人工來源作為 fallback。
- Loader 選擇順序為 NeoForge → Forge → Fabric；找不到時不得猜測。
- `content_id` 是 repository 目錄名稱，`mod_id` 是 Minecraft namespace，兩者不可互相推導。
- Flan 的英文來源是例外，固定至官方 GitHub commit 與明確語言檔路徑；設定保存在
  `config/mod-discovery-overrides.json`。

## 同步方向

- Upstream → Git：只更新 `metadata.json` 與 `en_us.json`。
- Git → ParaTranz：source PR 合併進 `main` 後才推送英文原文；現有遠端檔案以 manifest 的
  `file_id` 鎖定。新的 current `mod_id` 會建立遠端檔案，並以後續 PR 保存新 mapping。
- ParaTranz → Git：每小時先比較遠端 `modified_at`、最新 artifact 與 committed pull state；只有
  `pull_existing` 或 `generate_and_pull` 才下載、套用、建構與建立 `zh_tw.json` PR，`none` 直接結束。
- Manifest-only mapping 代表 repository 已移除但遠端仍存在的模組；工具只警告並保留 mapping、
  遠端檔案與譯文。任何 delete／prune 都由維護者人工確認與執行。
- Git commit 是建構與發布的唯一資料來源；發布時不得即時從 ParaTranz 下載未提交內容。
- Source-only commit 不觸發正式發布；只有拉回的新譯文進入 Git 後才發布。

## CI 切換狀態

舊 Beta／Release 與本庫內 reusable workflows 已退出版本控制。本庫已加入 source sync 與每小時
translation pull 的薄型 caller；更新偵測、同步 state、新模組 create／adopt 與保留刪除警告由
外部工具及 reusable workflow 實作。兩條 caller 共用 `project-9900` concurrency group，避免同一
ParaTranz project 的讀寫交錯。Toolkit version 預設留空，由集中安裝 action 取得 GitHub latest
release 並驗證 `SHA512SUMS`；正式成功執行仍需要 repository secrets 設定。
Caller 依照團隊既有翻譯包慣例引用 `reusable-workflows@v1`；本庫的 `zizmor.yml` 只對這個
TeamKugimiya 集中 workflow 允許 major-tag ref pin，其他第三方 Action 仍要求完整 commit SHA。

本階段不包含自動發布；ParaTranz pull 建立的翻譯 PR 合併後，只會成為可發布的 canonical Git 資料。
