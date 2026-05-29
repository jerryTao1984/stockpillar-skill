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
