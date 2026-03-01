---
name: openrca-rca-fastpath
description: 當需要在 OpenRCA 固定資料環境中，依告警症狀與時間快速收斂 root cause component、reason 與證據時觸發。此 Skill 採「假設矩陣 + 證據評分 + 反證排除」模式；查詢順序由訊號區分度與資料可靠性決定，不固定先看哪一層。固定使用 UTC+8，繁體中文輸出。主動更新時機：datasource/labels 變動時更新 environment-baseline；新增原子診斷能力時更新 query-packs；指標語意改動時更新 metrics-catalog；誤判案例出現時更新本檔的反模式與 guardrails。
---

# OpenRCA Fastpath RCA (Reframed)

## Goal

在最短且可重現的路徑內輸出可驗證結論：

1. root cause component
2. root cause reason
3. root cause occurrence time / exact time range
4. evidence
5. why_not_others

## Required Inputs

最小必要輸入如下：

1. `alert_message`（至少包含告警症狀與告警時間）
2. `expected_output_format`

可選輸入：

1. `component_metric_map`（若有，優先使用；若無，回退至 `references/environment-baseline.md` 與 `references/metrics-catalog.md`）

時區固定為 `UTC+8`（`Asia/Taipei`），不作為可變輸入。

## Core Principles

1. 先建立假設矩陣，再收斂；不得先假設特定元件或特定原因。
2. 查詢順序由「區分度」與「可靠性」決定，不採固定層級順序。
3. 每個候選都必須有正證據與反證據，且要有時間對齊。
4. 「查無 log」不可當成反證，只能視為弱證據或資料可用性問題。
5. 結論必須附信心與缺口，不可隱藏不確定性。

## Execution Policy

1. 優先使用固定環境基線（`references/environment-baseline.md`）。
2. 預設不做全量 discovery；僅在 query 空結果、label 不存在或資料不一致時啟用最小 discovery。
3. 回答語言固定繁體中文，並同時標示 UTC+8 與 UTC 時間。

## Workflow (Adaptive)

1. 時間收斂
以告警時間建查詢窗。
若輸入是區間，直接採用。
若輸入是單點，先查單點後 30 分鐘，必要時再向前回看 10-15 分鐘做根因定位。

2. 建立假設矩陣
至少建立 `component × reason` 的 3 個候選假設。
候選 reason 至少涵蓋：
`disk_space`, `disk_io`, `cpu`, `memory/jvm`, `network`, `db_availability`, `db_connection_limit`。

3. 選擇第一查詢層（非固定）
用以下準則選先查哪層：
`區分度高` 且 `資料可靠性高` 的層先查。
若某資料源存在一致性問題（例如 stats 與 logs 不一致），該層降級為佐證層，不作第一收斂層。

4. 執行證據查詢
依候選 reason 套用 `references/query-packs.md` 對應查詢。
先跑可直接反映原因的指標，再跑症狀指標與下游影響指標。

5. 反證與對照
每個候選至少附 1 組對照：
同類 peer component 對照，或替代原因排除（network/db/cpu 等）。
若只有單一資料源支持，不可直接定案。

6. 評分與收斂
為候選假設評分（高/中/低）：
直接原因指標 > 跨層時間對齊 > log 語意佐證。
選最高分為 rank 1，次高為 rank 2。

7. 固定格式輸出
依 `references/output-template.md` 輸出，不得省略 `why_not_others`。

## Query Pack Governance (Scale-up)

1. 不以「案例」擴張 query pack；以「原子診斷能力」擴張。
2. 新增 pack 的門檻：
現有 pack 無法表達該類原因，且此原因可跨元件重複使用。
3. 優先維護的 pack 類型：
`disk_space`, `disk_io`, `cpu`, `memory/jvm`, `network`, `db_availability`, `db_connection_limit`。
4. 元件差異放在 label/metric mapping，不放在新案例 pack。

## Guardrails

1. 不可只看單一 metric 下結論。
2. 不可把「查無 log」當成「無問題」。
3. 磁碟問題需區分 `disk_space` 與 `disk_io`，不可混用。
4. OOM 類問題不可只看重啟；必須同看 heap 壓力與 CPU/threads。
5. 稀疏或不連續 time series 只能作輔助證據，需搭配高可靠指標。
6. 結論必須標示時區（UTC+8 與 UTC）與信心等級。

## Known Anti-patterns

1. 先看症狀層（app/log）就快速定案，未先完成假設矩陣。
2. 把資料源查詢空結果直接當反證。
3. 不斷新增場景化 query packs，導致維護負擔與重疊規則。

## References

1. `references/environment-baseline.md`
2. `references/metrics-catalog.md`
3. `references/query-packs.md`
4. `references/output-template.md`
