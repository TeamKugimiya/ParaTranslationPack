# ParaTranz 結構遷移紀錄

狀態：遠端 path reconciliation 已完成；新同步工具與 workflow 已發布並通過本機 gate，等待新版 `reusable-workflows@v1` 與 secrets 驗證。

最後更新：2026-08-19

## 已完成

- 從舊 artifact 與 ParaTranz project `9900` 建立 157 份 canonical translation。
- 以模組實際最新版建立單一 tier，完成 157 筆合法且唯一的 `content_id`／`mod_id` mapping。
- 建立 `config/paratranz-files.json` schema 2，保存 157 筆唯一 `mod_id → file_id`。
- 將 157 個遠端檔案由 `MultiVersions/Forge/main/*.json` 改為
  `Translation/<content_id>/<tier>/<mod_id>.json`。
- 第一個 production canary 使用 Flan-Fabric：373 個詞條、5 筆繁中譯文，轉移前後所有
  term ID、key、original、translation、stage、context 與 source hash 完全一致。
- 其餘 156 個檔案全部 `confirmed`、0 `unknown`；沒有 create、delete、prune 或 source update。
- 批次前後 157 個 `terms_sha256` 與 remote source hash 完全一致。
- 最終 `doctor --remote`：157 checked、0 error、0 warning、0 repository-only、
  0 manifest-only、0 remote-only。
- 最終 source push dry-run：0 create、0 `reconcile_path`；所有 157 個 current path 已收斂。

## 稽核摘要

| 證據 | SHA-256／結果 |
| --- | --- |
| Identity manifest | `52dcad1e67e74e5f87769d7fb2fe13af034b6e902c406d1ead8cf906691d8a17` |
| 156-file apply journal | `b1a599fdd4391cd49650317c8a2ea4d345e8696a2df2389e845865219a961199` |
| Batch before/after evidence | `2772c9f881cf825e0951bc27ad31938044f63e189efc1ae2ed9ef4592e14ee9c` |
| Final remote inventory | 157 new paths、0 legacy paths、157 unique file IDs |
| Final remote doctor | 0 error、0 warning |
| Final reconciliation | 0 create、0 path mismatch |

完整 journal、API snapshots、來源 ZIP、轉換器與測試只保存在本機 migration workbench，不提交，
且不得包含 token。這些內容在穩定上線前由 `.gitignore` 保留；穩定後可移至不可變外部封存或刪除。

## 2026-08-18 自動化驗證

- `paratranz-toolkit` 的 build、format、vet、lint、staticcheck、govulncheck、race unit、built-binary
  E2E 與 module tidy gate 全數通過。
- Production project 的唯讀 source push dry-run 已收斂：157 files、44,381 keys、0 create、
  0 update、0 path reconciliation、0 retained mapping。
- Production update check 回報 `pull_existing`：latest artifact `1687398` 已新鮮，但 repository 尚無
  committed state；首次完整 pull 會建立 state，合併後無遠端更新的每小時排程將回報 `none`。
- Reusable workflow 文件產生與 zizmor low-severity gate 通過。
- 新 current `mod_id` 的 create、逐檔 manifest publish、嚴格 adopt recovery，以及 manifest-only
  retained warning 已由 mock contract、unit 與 built-binary E2E 覆蓋；工具沒有 delete／prune API 路徑。

## 2026-08-20 首次 source sync 實際執行

- Source sync workflow 首次在 project `9900` 端到端跑通。`paratranz-tool v0.2.0`、
  `reusable-workflows v1.7.1`；dry-run 與 apply 皆 `ok`，push 前後的 `doctor --remote` 皆 `ok`。
- 結果為 0 mutation：157 files、44,381 keys 全數 unchanged，`remote_changed: false`，
  0 create、0 adopt、0 path reconciliation、0 update source、0 unknown、0 pending、0 term delete。
  遠端在此前的 path reconciliation 之後即已收斂，本次沒有對 ParaTranz 寫入任何內容。
- `state_precondition: "missing"` → `state_status: "published"`：首次建立 source state，
  並以 bot PR 提交 `config/paratranz-source-state.json`。合併後後續執行才能使用 Terms fast-skip。
- 在此之前該 workflow 固定失敗於「規劃 ParaTranz source push」：下游 jq gate 沿用了
  `sync pull-translation` 的 state 詞彙，但 `sync push-source` 的 dry-run 對缺少 state 回報
  `missing`、對無差異回報 `valid`，兩者都不在 gate 接受的值域內。由於 source state 只能由
  `--apply` 建立，而 `--apply` 又被失敗的 dry-run gate 擋下，首次執行永遠無法啟動。
  已由 `paratranz-toolkit SPEC 20`／`v0.2.0`（統一兩個 mode 的詞彙、report schema 升為 8）與
  `reusable-workflows v1.7.1`（gate 接受 `missing` 並斷言 schema 8）修正。
- `TOOLKIT_TOKEN` 與 `PARATRANZ_TOKEN` 已由本次執行實證可用；`CURSEFORGE_API_KEY` 尚未驗證，
  本次 `sync_sources` 為 false，模組來源更新步驟被跳過。

## 尚未完成的上線閘門

- 驗證 `CURSEFORGE_API_KEY`：需要一次 `sync_sources` 為 true 的執行（schedule 或
  `workflow_dispatch`）才會實際使用。
- 確認下一次無更新排程使用已提交的 `config/paratranz-sync-state.json`，並跳過 artifact generation、
  pull、build 與 PR。
- 以一個測試／新模組完成 production create canary，確認 manifest PR 合併後重跑為 no-op。
- 完成一次真正有 source 差異的 push：新增 key、更新原文與移除 key 的行為仍未在 project `9900`
  實測，首次 apply 是 0 mutation。
- 驗證 source-only 不發布、translation pull PR 合併後才發布，且不會形成 commit／dispatch 迴圈。
- 完成一次正常發布週期後，將本機忽略的舊 Python scripts、package 設定與遷移 workbench
  移至不可變外部封存或刪除。
