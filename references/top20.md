# StockPillar Top20 Reference

## `/top20/daily` Guide

Use `GET /top20/daily?trade_date=YYYYMMDD&type=score_top20|prediction_top20` or `GET /top20/daily?previous_trade_date=true&type=...` when the user asks for:

- 某个交易日的 `score_top20`
- 某个交易日的 `prediction_top20`
- 某个交易日的兄弟公司榜单归档
- 每日 top20 股票名单
- AI 点评是否已经落库

### Required Parameters

- You must provide one of:
- `trade_date`: explicit target trade date, format `YYYYMMDD`
- `previous_trade_date=true`: ask the backend to resolve the previous trading day automatically

### Optional Parameters

- `type`: optional, supports `score_top20` or `prediction_top20`
- `previous_trade_date=true`: optional shortcut for "上一个交易日". Prefer this when the user asks for the previous trading day's榜单, rather than asking the agent to calculate the date
- If `type` is omitted, the backend will try both list types
- If `type` is provided, the backend only queries that one list and will not touch the other upstream endpoint
- Prefer passing `type` when the user only needs one list, especially for `prediction_top20` or `score_top20` single-purpose queries
- If both `trade_date` and `previous_trade_date=true` are sent, `trade_date` wins

### Response Shape

The response data contains:

- `trade_date`: requested trade date
- `snapshot_date`: local fetch date
- `lists.score_top20`: cached or freshly fetched score top20
- `lists.prediction_top20`: cached or freshly fetched prediction top20
- `errors`: list of partial failures

Each list payload contains:

- `source_trade_date`
- `agent_trade_date`
- `item_count`
- `items`

Each top20 item includes:

- `stock_code`
- `stock_name`
- `industry`: original industry label for finer-grained analysis
- `tier`: normalized config tier derived from `industry`, suitable for higher-level grouping
- `score_top20` items also include `close_price` / `pct_chg_pct` / `score_value`
- `prediction_top20` items also include `avg_score` / `avg_rank` / `agent_decision` / `agent_score` / `agent_summary`

### Behavior Rules

- The backend queries strictly by `trade_date`.
- When `previous_trade_date=true`, the backend resolves the previous trading day from the trading calendar and then queries strictly by that resolved trade date.
- If `type` is provided, the backend only checks that one list type.
- If the external source returns a different trade date, the backend will not use it as a substitute.
- If no matching trade-date data exists, the result may be empty for that list.
- Use `industry` for finer-grained industry analysis and `tier` for higher-level grouping; do not treat them as the same field.
- `score_top20` is currently stable.
- `prediction_top20` depends on the upstream AI pipeline and may time out, return `502`, or return `503`.
- When `prediction_top20` is unavailable, read `errors` and continue using `score_top20` if present.
- If `type` is invalid, the API returns `400`.

### Agent Output Guidance

- Always state the requested `trade_date`.
- Distinguish `score_top20` and `prediction_top20`; they are not the same ranking.
- If `prediction_top20` is missing, explicitly say the upstream AI endpoint was unavailable for that date.
- Do not claim that another trade date is equivalent.
