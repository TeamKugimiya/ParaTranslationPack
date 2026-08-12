# ParaTranz 結構遷移紀錄

狀態：遠端 path reconciliation 已完成；source update 與自動化切換尚未啟用。

日期：2026-08-12

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

## 尚未完成的上線閘門

- `paratranz-toolkit sync push-source --apply` 尚待 mutation transport contract、manifest recovery
  contract 與專用測試 project canary；目前仍有 105 個 source update plan，不得用 bootstrap 腳本處理。
- 完成 `sync pull-translation` 的正式 artifact／path 驗證與有差異、無差異 canary。
- 在集中 repository 發布固定版本 reusable workflows，讓本庫只保存 thin callers。
- 驗證 source-only 不發布、translation pull 才發布，且不會形成 commit／dispatch 迴圈。
- 完成一次正常發布週期後，將本機忽略的舊 Python scripts、package 設定與遷移 workbench
  移至不可變外部封存或刪除。
