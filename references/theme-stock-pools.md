# StockPillar Theme Stock Pools Reference

This module is for versioned, stored theme stock pools. It is separate from the
event/theme overlay endpoints in `industries-events.md`.

Use this module when the user asks for:

- 主题池清单 / 有哪些主题池
- 某个主题池有哪些版本
- 某个版本的主题池股票
- 按 L1/L2/L3/L4/L5 层级查询主题池
- 主题池股票按模型评分或排名排序
- 主题池版本之间的成员查看或人工研究池查询
- 发起 / 查看股票池有效性诊断（四关体检：是不是真 β、独立性、稳定性、性价比）

Do not use this module for:

- 今天某主题为什么强弱变化
- 某主题的事件催化或风险解释
- 主题 overlay、daily brief、event evidence
- 日期绑定的 overlay preferred basket

For those requests, use `industries-events.md`.

## Core Semantics

- `/themes/{theme_code}/stocks` is a date-bound overlay preferred basket.
- `/themes/{theme_code}/stock-pool*` is versioned stored pool data.
- These two families are not interchangeable.
- Versioned pool queries are keyed by `theme_code` plus optional `source_version`.
- If `source_version` is omitted, the backend resolves the current/latest version.
- If `level_code` is omitted, return all levels. Do not default-exclude `L5`.
- `level_code` supports one value or multi-select values.
- Do not reuse the AI event default `AI_EMBODIED` for versioned pool queries unless the
  user explicitly names it. If the user only says "AI 主题池", first call
  `/theme-stock-pools` or use the pool code shown by that endpoint.

## Endpoint Choice

- `GET /theme-stock-pools`: list available versioned theme pools. Use this when the user
  asks what pools exist, or when the user did not provide a `theme_code`.
- `GET /themes/{theme_code}/stock-pool/versions`: list versions for one theme pool. Use
  this when the user asks for version numbers or latest/current version discovery.
- `GET /themes/{theme_code}/stock-pool`: fetch stored pool members. Use this for version,
  layer, segment, or core-type filtering.
- `GET /themes/{theme_code}/stock-pool/ranked`: fetch stored pool members sorted by model
  score or rank. Use this when the user asks for scoring/ranking/TopN within a theme pool.
- `POST /themes/{theme_code}/stock-pool/diagnostics`: start an async pool-effectiveness
  diagnostic ("四关体检"). Use when the user asks to run/launch a diagnostic on a pool.
- `GET /themes/{theme_code}/stock-pool/diagnostics`: list a version's diagnostic runs with
  status. Use to check progress or show how many diagnostics exist.
- `GET /themes/{theme_code}/stock-pool/diagnostics/{run_id}`: fetch one run's full four-gate
  report. Use to show a finished diagnostic's metrics and conclusion.

## Parameters

### `/theme-stock-pools`

Required:

- none

Optional:

- none

Response:

- rows are under `data.records`
- each row identifies a versioned pool and usually includes `theme_code`, `pool_name`,
  version/status fields, and counts where available

### `/themes/{theme_code}/stock-pool/versions`

Required:

- path `theme_code`

Optional:

- `limit`: maximum version rows to return

Use:

- omit `limit` unless the user asks for only recent versions
- use this before a version-specific query when the user says "最新版本" and you need to
  show or confirm the resolved version

### `/themes/{theme_code}/stock-pool`

Required:

- path `theme_code`

Optional:

- `source_version`: omit for current/latest version
- `level_code`: one layer such as `L1`, or multi-select such as `L1,L2,L3`; repeated
  query params are also supported by the backend
- `segment_code`: filter by supply-chain/industry segment
- `core_type`: filter by core type such as `L1A` or `L1B` when present
- `page`
- `size`

Use:

- ask for this endpoint when the user wants raw members by pool/version/layer
- omit `level_code` for all levels
- do not filter out `L5` unless the user asks to exclude it

### `/themes/{theme_code}/stock-pool/ranked`

Required:

- path `theme_code`

Optional:

- `source_version`: omit for current/latest version
- `level_code`: one layer or multi-select (`L1,L2`, repeated params)
- `trade_date`: scoring date; omit to let the backend resolve the default scoring date
- `is_active`: default active score rows; pass `all` only if the user asks to include
  inactive score rows
- `page`
- `size`

Use:

- this endpoint is the default for "按评分排序", "排名", "TopN", "模型分", or
  "score/rank" questions inside a versioned theme pool
- if the user gives both level and ranking requirements, keep both filters
- if the user does not pass `source_version`, omit it rather than guessing one

### Diagnostics (四关体检)

The diagnostic validates whether a pool is a real, usable β unit, across four gates:
关1 内部凝聚力, 关2 与基准独立性, 关3 β 稳定性, 关4 β 性价比. It is **asynchronous**.

`POST /themes/{theme_code}/stock-pool/diagnostics`

Required:

- path `theme_code`
- JSON `source_version`

Optional:

- JSON `level_code`: array or comma string (e.g. `["L1","L2","L3"]`); omit = all non-L5 layers
- JSON `end_date`: `YYYYMMDD` scoring window end; omit = latest trade day

`GET /themes/{theme_code}/stock-pool/diagnostics`

- optional `source_version` (omit = current/latest), `limit` (default 50)
- returns runs newest-first under `data.records`; `data.total` = run count

`GET /themes/{theme_code}/stock-pool/diagnostics/{run_id}`

- returns one run; on `SUCCESS` the `report` object holds the full four-gate metrics

Use (async lifecycle — important):

- `POST` returns `{run_id, status:"PENDING"}` **immediately**; the diagnostic runs ~1-2 minutes
  in the background. **Do not block on the POST or treat its response as the result.**
- Poll the list endpoint until `status` is `SUCCESS`/`FAILED`, then fetch the detail by `run_id`.
- Do not launch repeated runs for the same version while one is `PENDING`/`RUNNING`.
- A `FAILED` run carries `error_message` (e.g. `行情或指数数据不足` when the chosen level subset has
  too few members or too short a common window).

Gate thresholds (for interpreting `report`):

- 关1: `rho_median` (>0.5 PASS / 0.3-0.5 WARN / <0.3 FAIL) + `pc1_ratio` (>50% / 30-50% / <30%)
- 关2: `r_squared` decides — **>0.85 FAIL (就是基准)**, 0.6-0.85 WARN, <0.6 PASS; `beta`+CI and
  `alpha_annual_linear` are reported only
- 关3: `beta_cv` (<0.3 / 0.3-0.5 / >0.5); if `beta_cv_applicable=false` judge by `beta_range`
  (<0.6 / 0.6-1.0 / >1.0)
- 关4: `sharpe` (>0.5 / 0.2-0.5 / <0.2), `information_ratio` (>0.3 / 0.1-0.3 / <0.1),
  `max_drawdown` (<25% / 25-40% / >40%); all three must PASS

`overall_conclusion` (server-derived, do not recompute):

- 全 PASS → 可作为 β 池裸持
- 关1-3 PASS、关4 WARN/FAIL → 合法 β 但需叠 α
- 关3 FAIL → 仅短期使用，须设退出条件
- 关2 FAIL（R²>0.85）→ 不是独立 β，弃用或重定义
- 关1 FAIL → 池子定义无效，必须重做

When answering, state the 范围 (version, level scope, `window_start`~`window_end`,
`member_count_effective`/`member_count_raw`), the 基准 (`benchmark_name`), the four gate statuses,
the conclusion, and the `pressure_windows` (微盘崩盘 / 中特估退潮 / 上海疫情) for tail risk.

## Important Fields

Versioned pool member rows include:

- `theme_code`
- `source_version`
- `ts_code`
- `stock_name`
- `level_code`
- `level_name`
- `segment_code`
- `segment_name`
- `core_type`
- `operation_suggestion`
- classification and evidence fields when available

Ranked rows additionally include:

- `score_trade_date`
- `score_source`
- `score_rank`
- `rank_key`
- `score_key`
- model score/rank fields when available

Endpoint-level ranked metadata can include:

- `score_trade_date`
- `score_source`
- `pool_count`
- `ranked_count`
- `records`

## Output Guidance

When answering from versioned theme pool endpoints:

- state the `theme_code`
- state the `source_version`; if omitted in the request, say the backend resolved latest/current
- state the `level_code` filter, or say all levels were included
- state the scoring date when using `/ranked`
- distinguish stored pool membership from event-driven theme opinion
- do not describe membership as a buy/sell recommendation unless another policy skill adds that layer

## Common Examples

List pools:

```bash
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/theme-stock-pools"
```

List versions:

```bash
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool/versions?limit=50"
```

Query L1/L2 members:

```bash
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool?source_version=V2.0&level_code=L1,L2&page=1&size=50"
```

Query ranked members:

```bash
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool/ranked?source_version=V2.0&level_code=L1,L2,L3&page=1&size=50"
```

Start a diagnostic, then poll for the result:

```bash
# 1) start (returns {run_id, status:"PENDING"})
curl -s -X POST -H "Authorization: Bearer $STOCKPILLAR_API_KEY" -H "Content-Type: application/json" \
  -d '{"source_version":"V2.0","level_code":["L1","L2","L3"]}' \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool/diagnostics"

# 2) poll the list until status=SUCCESS
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool/diagnostics?source_version=V2.0"

# 3) fetch the full four-gate report
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/themes/AI_FULL_CHAIN/stock-pool/diagnostics/123"
```
