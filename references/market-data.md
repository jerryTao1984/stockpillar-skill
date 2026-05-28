# StockPillar Market Data Reference

## Agent Decision Shortcut

Follow this shortcut before reading endpoint details:

- "现在 / 当前 / 最新 / 实时行情 / 盘中价格" -> `/prices/realtime`.
- "个股主力资金 / 个股净流入 / 个股资金趋势" -> `/stocks/{ts_code}/moneyflow`.
- "北向资金 / 沪深港通资金流 / 外资今天买卖" -> `/moneyflow/hsgt` or `/moneyflow/hsgt/overview`.
- "北向持仓 / 港股通持股比例 / 外资持股量" -> `/stocks/{ts_code}/flows/hk-hold`.
- "融资融券 / 两融余额" -> `/margin/summary`, `/margin/detail`, or `/stocks/{ts_code}/margin`.
- "日度市场状态 / 今天适不适合开仓" -> `/market/summary` or `/market/summary/v2`.
- "盘中情绪 / 当前市场热度 / 追强环境" -> `/market/sentiment_pulse` or `/market/sentiment_pulse/v2`.

Semantic rule:

- `flow` means money movement.
- `holding` means ownership or position.
- Do not mix HSGT moneyflow and HSGT holding endpoints.

## Market Supplement Endpoint Rules

Use the supplemental market endpoints when the user asks for facts that affect tradability, flow ownership, or event risk rather than price/indicator interpretation.

Endpoint selection:

- `GET /stocks/{ts_code}/prices/limits`: daily `up_limit` and `down_limit`; use for涨停价、跌停价、回测成交约束、是否接近涨跌停.
- `GET /stocks/{ts_code}/events/suspend`: suspension/resumption records; use for停牌、复牌、不可交易原因.
- `GET /stocks/{ts_code}/flows/hk-hold`: HSGT holding records; use for北向/港股通持股比例、持股量变化. Do not confuse it with `/moneyflow/hsgt`, which is market flow.
- `GET /stocks/{ts_code}/events/share-float`: restricted-share unlock records; use for解禁日期、解禁股数、股东、股份类型.
- `GET /stocks/{ts_code}/technical/cyq-perf`: chip distribution reference metrics; use for成本分位、平均成本、获利盘比例.
- `GET /stocks/{ts_code}/technical/cyq-chips`: chip distribution buckets; use for价格档筹码占比.
- `GET /stocks/{ts_code}/events/limit-list`: daily limit-up/down board records; use for连板、开板次数、封单强度、涨跌停类型.
- `GET /stocks/{ts_code}/events/surveys`: institution survey records; use for调研机构、接待地点、接待人员、调研内容.
- `GET /stocks/{ts_code}/flows/slb-sec-detail`: securities lending records; use for转融券期限、费率、数量.
- `GET /concepts/{ts_code}/moneyflow/ths`: THS concept moneyflow; use for概念板块资金流 and distinguish it from stock-level `/stocks/{ts_code}/moneyflow`.

Response shape:

- All supplemental endpoints return `data.records`.
- Each response also carries the path `ts_code`.
- Date fields inside records are authoritative; for share-unlock data, prefer `float_date` over `trade_date`.

Output guidance:

- State the exact date or date range used.
- For limit prices, distinguish `up_limit/down_limit` from actual `high/low/close`.
- For suspension data, absence of records in the requested range means no matched suspension rows in the local database, not proof that the stock was always tradable in all venues.
- For HSGT holding, describe it as holdings/ownership, not same-day buying amount.
- For share unlocks, mention `float_share`, `float_ratio`, `holder_name`, and `share_type` when present.
- For chip distribution, distinguish reference summary metrics (`cyq-perf`) from price-bucket detail (`cyq-chips`).
- For securities lending, describe `lending_rate` as fee/rate and `vol` as quantity.
- For THS concept moneyflow, state that `ts_code` is a concept code, not necessarily an A-share stock code.

## Endpoint Rules

### `/prices/realtime`

Use when:

- the user asks `现在`, `当前`, `最新`, `盘中`, or `实时行情`
- the user wants latest price, intraday change, bid/ask, or turnover

Do not use when:

- the user wants historical走势 or K-line
- the user wants a technical signal event

Example user asks:

- `现在贵州茅台多少钱`
- `帮我看 600519.SH 的实时行情`
- `比较一下茅台和五粮液当前涨跌`

Required params:

- `ts_codes`

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/prices/realtime?ts_codes=600519.SH,000858.SZ" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- always include the latest price and pct change
- if `pct_chg` is absent, compute it from `price` and `pre_close`
- use `trade_time` as the practical timestamp when `update_time` is absent
- for multiple securities, present them side by side
- do not describe realtime data as end-of-day confirmed close

### `/stocks/{ts_code}/moneyflow`

Use when:

- the user asks about 主力流入流出, 资金净流入, or recent capital flow for one stock
- the user wants a short-period资金趋势

Do not use when:

- the user asks about northbound/southbound aggregate flow
- the user asks for price-only走势

Example user asks:

- `贵州茅台最近一周资金流向怎么样`
- `600519.SH 今天主力是净流入还是净流出`

Required params:

- `ts_code`
- `start_date`
- `end_date`

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/moneyflow?start_date=20260407&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- specify the date range first
- summarize net inflow/outflow direction
- highlight whether the latest day agrees with the short-term trend
- avoid overinterpreting one noisy day as a confirmed reversal

### `/moneyflow/hsgt`

Use when:

- the user asks about northbound, southbound, or 沪深港通 aggregate capital flow
- the user wants market-level cross-border flow over a date range

Do not use when:

- the user asks about one stock's capital flow
- the user omits the date range and expects the API to infer it

Example user asks:

- `最近一周北向资金净流入怎么样`
- `查一下 20260407 到 20260416 的沪深港通资金`

Required params:

- `start_date`
- `end_date`

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt?start_date=20260407&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- always state the queried date range
- summarize the aggregate net inflow/outflow direction
- if the response is multi-day, mention whether flow strengthened or weakened across the window

### `/moneyflow/hsgt/overview`

Use when:

- the user asks for one-day northbound summary
- the user wants 当日北向整体净流入、沪股通/深股通拆分
- the user wants the current day's top active northbound stocks

Do not use when:

- the user asks for a multi-day trend window only
- the user wants one stock's own capital-flow history

Example user asks:

- `看一下 20260417 北向资金整体流入情况`
- `给我 4月17日的沪股通、深股通汇总和前十大活跃股`

Optional params:

- `trade_date`: one trading day in `YYYYMMDD`
- `days`: optional trend length for the embedded recent trend block
- if `trade_date` is omitted, the backend resolves the latest available trading day from the stored summary or Top10 data

Request:

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt/overview?trade_date=20260417&days=5" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- lead with `north_money`, `hgt`, and `sgt`
- summarize `market_breakdown` for 沪股通 and 深股通 separately
- `top10_records` is the flat record list
- `top10_by_market` is the grouped view derived from the same records
- when the user asks about active names, prefer `top10_records` for ranking detail and `top10_by_market` for沪/深 grouping
- if `buy_amount`, `sell_amount`, or `net_amount` are empty, say the upstream source did not provide them

### `/moneyflow/hsgt/top10`

Use when:

- the user asks for 北向前十大活跃股
- the user wants to filter by 沪股通 or 深股通
- the user wants top10 records for a date range or one stock in the ranking history

Do not use when:

- the user only wants aggregate northbound net inflow/outflow

Common params:

- `trade_date`: best for one-day top10 snapshot
- `start_date` + `end_date`: best for historical range queries
- `market_type`: `1` for 沪股通, `3` for 深股通
- `ts_code`: optional stock filter
- `page`, `size`

Request:

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt/top10?trade_date=20260417&market_type=1" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- group or label records by `market_type`
- highlight `rank_no`, `turnover_amount`, and stock name/code first
- mention `buy_amount`, `sell_amount`, and `net_amount` when present
- if those three fields are empty, say the upstream source returned blanks for that date

### `/margin/summary` and `/margin/detail`

Use when:

- the user asks about 融资余额, 融资买入额, 融资偿还额, 融券余额, 融资融券余额
- the user wants market-wide margin snapshot by exchange
- the user wants one stock's margin-detail history or a single trading day's margin-detail ranking

Choose the endpoint like this:

- `GET /margin/summary`: exchange-level summary rows for one day or a date range
- `GET /margin/detail`: stock-level detail rows; can filter by `ts_code`
- `GET /stocks/{ts_code}/margin`: prefer this canonical path when the user clearly asks about one stock

Common params:

- `trade_date`: best for one-day queries
- `start_date` + `end_date`: best for trends or history
- `exchange_id`: only for `/margin/summary`, allowed values `SSE`, `SZSE`, `BSE`

Example requests:

```bash
curl "$STOCKPILLAR_API_URL/margin/summary?trade_date=20260417" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

```bash
curl "$STOCKPILLAR_API_URL/margin/detail?trade_date=20260417&ts_code=600519.SH" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/margin?start_date=20230101&end_date=20260417" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- always state whether the answer is exchange-level summary or stock-level detail
- always state the trade date or date range
- for stock detail, prioritize `rzye`, `rzmre`, `rzche`, `rqye`, and `rzrqye`
- for summary, compare exchanges only if the same trade date is being discussed
### `/market/summary`

Use when:

- the user asks for a daily market score or a daily market state summary
- the user wants an agent-friendly daily market regime assessment rather than a raw market snapshot
- the task needs structured outputs such as subscores, risk flags, and action guidance
- the user or calling code prefers the explicit versioned path `/market/summary/v2`; it currently returns the same v2 payload

Do not use when:

- the user wants intraday pulse or live temperature only
- the user asks for one stock or one industry only

Example user asks:

- `今天 A 股市场状态怎么样`
- `给我一个日度市场评分`
- `今天适不适合开新仓`

Required params:

- none

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/market/summary" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Versioned request:

```bash
curl "$STOCKPILLAR_API_URL/market/summary/v2" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- treat this endpoint as the canonical daily market-state payload for agents
- lead with `market_score` and `market_state`
- then read `subscores` in this order: `breadth_score`, `strength_score`, `risk_score`, `flow_score`
- inspect `risk_flags` before acting on the total score
- use `agent_guidance` directly when the task is about whether to open new positions, reduce size, or stay selective
- support the answer with `metrics` and `explanation`

Response shape:

- `trade_date`: daily market regime date
- `mode`: always `daily`
- `market_score`: normalized overall market score in the `0-100` range
- `market_state`: daily regime label such as `极强`, `偏强`, `偏强分化`, `震荡`, `偏弱`, `高风险弱势`
- `subscores`:
  - `breadth_score`: market breadth and diffusion
  - `strength_score`: short-term attack strength and leader expansion
  - `risk_score`: downside risk score; higher means safer
  - `flow_score`: capital and turnover confirmation
- `metrics`: raw supporting facts such as `up_count`, `down_count`, `up_ratio_pct`, `limit_up_count`, `limit_down_count`, `strong_up_count`, `strong_down_count`, `avg_pct_chg`, `main_net_flow_bn`, `total_amount_bn`, and `volume_ratio_vs_20d`
- `risk_flags`: hard constraints such as `risk_off`, `limit_down_risk`, `strong_divergence`, `weak_rebound`, `rotation_fast`, `speculation_overheat`, and `no_flow_confirmation`
- `agent_guidance`:
  - `can_open_new_positions`
  - `should_reduce_position_size`
  - `prefer_leaders_only`
  - `avoid_bottom_fishing`
  - `allow_aggressive_breakout`
- `explanation`: 1 to 3 short Chinese sentences that summarize why the score looks the way it does

Agent rules:

- Use `risk_flags` as hard overrides before trusting the total score.
- Treat `risk_score` as a safety score: higher is safer, lower is riskier.
- When `limit_down_risk` or `risk_off` is present, do not let a mid-to-high `market_score` override the warning.
- Prefer `agent_guidance` over custom heuristic rewrites unless the user explicitly asks for your own judgment.

Example response excerpt:

```json
{
  "trade_date": "2026-04-21",
  "mode": "daily",
  "market_score": 54.26,
  "market_state": "震荡",
  "subscores": {
    "breadth_score": 38.64,
    "strength_score": 80.85,
    "risk_score": 60.0,
    "flow_score": 22.74
  },
  "risk_flags": [
    "limit_down_risk",
    "no_flow_confirmation",
    "rotation_fast"
  ],
  "agent_guidance": {
    "can_open_new_positions": false,
    "should_reduce_position_size": true,
    "prefer_leaders_only": true,
    "avoid_bottom_fishing": true,
    "allow_aggressive_breakout": false
  },
  "explanation": [
    "下跌家数占优，市场宽度偏弱。",
    "涨停和强势股数量较多，短线攻击性仍在。",
    "跌停或大跌扩散偏多，风险端仍需控制。"
  ]
}
```

### `/market/sentiment_pulse`

Use when:

- the user asks about intraday market mood, risk appetite, 热度, or live market state
- the user wants an agent-friendly intraday market score with risk flags and guidance
- the task depends on whether the current盘中 environment supports aggressive trading
- the user or calling code prefers the explicit versioned path `/market/sentiment_pulse/v2`; it currently returns the same v2 payload

Do not use when:

- the user only wants a daily post-close market assessment
- the user asks for one stock-level analysis

Example user asks:

- `现在市场情绪怎么样`
- `盘中风险偏好是回升还是走弱`
- `当前环境适不适合追强`

Required params:

- none

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/market/sentiment_pulse" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Versioned request:

```bash
curl "$STOCKPILLAR_API_URL/market/sentiment_pulse/v2" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- treat this endpoint as the canonical intraday market-state payload for agents
- lead with `market_score` and `market_state`
- then read `subscores` in this order: `breadth_score`, `strength_score`, `risk_score`, `flow_score`
- inspect `risk_flags` before acting on the total score
- use `agent_guidance` directly when the task is about whether to open new positions, reduce size, prefer leaders only, or avoid bottom-fishing
- support the answer with `metrics` and `explanation`

Response shape:

- `trade_date`: usually `null` for live intraday snapshots
- `mode`: always `intraday`
- `market_score`: normalized intraday market score in the `0-100` range
- `market_state`: intraday regime label such as `极强`, `偏强`, `偏强分化`, `震荡`, `偏弱`, `高风险弱势`
- `subscores`:
  - `breadth_score`: live diffusion and red-green balance
  - `strength_score`: 5%+ movers and live attack strength
  - `risk_score`: live downside risk score; higher means safer
  - `flow_score`: intraday order-flow and bid-side support
- `metrics`: raw supporting facts such as `up_count`, `down_count`, `p_zero_count`, `up_ratio_pct`, `limit_up_count`, `limit_down_count`, `strong_up_count`, `strong_down_count`, `temperature_legacy`, `total_amount_bn`, `order_imbalance_pct`, `market_bid_ratio`, `last_update`, and `is_live`
- `risk_flags`: hard constraints such as `risk_off`, `limit_down_risk`, `strong_divergence`, `weak_rebound`, `rotation_fast`, `speculation_overheat`, and `no_flow_confirmation`
- `agent_guidance`:
  - `can_open_new_positions`
  - `should_reduce_position_size`
  - `prefer_leaders_only`
  - `avoid_bottom_fishing`
  - `allow_aggressive_breakout`
- `explanation`: 1 to 3 short Chinese sentences that summarize the live market condition

Agent rules:

- Use this endpoint for current intraday conditions, not post-close narrative review.
- `temperature_legacy` is a compatibility metric; prefer `market_score` plus `subscores` for decisions.
- `is_live=false` means the snapshot is stale. Report that explicitly before making time-sensitive recommendations.
- As with the daily endpoint, treat `risk_flags` as hard overrides before trusting the total score.

Example response excerpt:

```json
{
  "trade_date": null,
  "mode": "intraday",
  "market_score": 65.32,
  "market_state": "偏强分化",
  "subscores": {
    "breadth_score": 47.65,
    "strength_score": 93.25,
    "risk_score": 55.83,
    "flow_score": 63.33
  },
  "metrics": {
    "temperature_legacy": 73,
    "order_imbalance_pct": 15.8,
    "is_live": false
  },
  "risk_flags": [
    "limit_down_risk",
    "rotation_fast"
  ],
  "agent_guidance": {
    "can_open_new_positions": false,
    "should_reduce_position_size": true,
    "prefer_leaders_only": true,
    "avoid_bottom_fishing": true,
    "allow_aggressive_breakout": false
  },
  "explanation": [
    "盘中多空仍在拉扯，扩散度一般。",
    "5%以上强势股较多，短线情绪较活跃。",
    "跌停或大跌扩散尚未出清，盘中风险仍在。"
  ]
}
```

## `/risk-events/*` and `/market/regime_events` Guide

Use these when the user asks about market-level or stock-level *risk* signals — regulatory,
delisting, fraud, hard-risk alerts, or regime shifts that justify reducing exposure.

### Endpoint Choice

- `GET /market/regime_events`: market-state-shift risk evidence aggregated for the configured
  trade_date (defaults to latest). Use when the user asks 「市场要不要砍仓 / 是不是变天 / regime shift」.
- `GET /risk-events/market`: chronological feed of market-level risk events (policy tightening,
  geopolitics, liquidity shock). Use when the user wants a *list* of risk events over a date range.
- `GET /risk-events/stocks`: per-stock risk events (退市风险、立案调查、问询函、关联方占用、违规处罚).
  When the user asks about a specific stock's *risk* (not earnings/event in general), prefer this
  over `/stocks/{ts_code}/events` — it covers compliance/regulatory signals that the general
  event feed may not surface.

### Required and Optional Parameters

- `/market/regime_events`: optional `trade_date`, `risk_level`, `risk_domain`, `limit` (default
  50), `offset` (default 0). No required params.
- `/risk-events/market`: optional `start_date`, `end_date`, `risk_level`, `risk_domain`,
  `page`, `size` (default 50, max 500).
- `/risk-events/stocks`: optional `start_date`, `end_date`, `ts_code`, `stock_name`,
  `risk_level`, `risk_category`, `page`, `size` (default 50).

### Field Vocabulary

- `risk_level`: `hard` (硬风险，立刻规避), `soft` (软风险，提示性), `none`.
- `risk_domain`: typically one of `regulation`, `delisting`, `compliance`, `liquidity`,
  `geopolitics`, `macro`, `corporate_governance` — confirm from response, do not hardcode.
- `risk_category`: stock-side category (e.g. `INVESTIGATION`, `DELISTING_WARNING`, `INQUIRY_LETTER`,
  `PLEDGE_RISK`, `RELATED_PARTY_DIVERSION`).

### Interpretation Rules

- Cross-check with `/stocks/{ts_code}/events?risk_level=hard` — the two feeds overlap but
  `/risk-events/stocks` is the canonical risk-curated surface.
- When user asks 「今天有哪些硬风险」 → call `/risk-events/market` and
  `/risk-events/stocks` with `risk_level=hard` and the current trade date range.
- These endpoints back the **sell-rule layer-0 risk overlay** — when used in that context, prefer
  newest-first by publish time and surface `ts_code`, `risk_category`, `risk_level`, `publish_time`,
  source URL.
- Do not treat the absence of risk events as proof of safety; say "未发现已登记的风险事件"
  rather than "无风险".

### Hook For Sell-Rule / dolphinagent Policy Skill

When a sell-side policy skill is loaded alongside this one (e.g. dolphinagent or a future
sell-rule skill), this section is the **canonical entrypoint** for layer-0 黑天鹅事件 evidence.

Context that policy skill should treat as load-bearing:

- The partner company's selection pipeline does **not** consume regulatory/delisting events —
  their `event_flags` are purely technical. Full plan and rationale live in
  `docs/SELL_RULE_DESIGN.md` (project-side, not duplicated here).
- The sell rule is a six-layer cascade: Layer 0 (黑天鹅事件) → Layer 1 (硬止损) → Layer 2
  (risk_score 突变) → Layer 3 (信号衰减) → Layer 4 (排名跌出 top100) → Layer 5 (跟踪止盈) →
  Layer 6 (20 天兜底). Layer 0 is the **highest priority and lowest infra cost**, and these
  endpoints are exactly its data spine.
- Selection alpha belongs to the partner; risk events belong to us. The sell-rule skill should
  **only** consume risk endpoints (`/risk-events/*`, `/market/regime_events`, optionally
  `/stocks/{ts_code}/events?risk_level=hard`) for layer-0 decisions, **not** call back into
  `/screen/stocks` or `/top20/daily` for "re-selection".

Recommended call pattern from a sell-rule skill, given a current position list:

1. `GET /risk-events/market?start_date=<today-3>&risk_level=hard` → market-wide regime risk.
2. For each held `ts_code`: `GET /risk-events/stocks?ts_code=<ts_code>&risk_level=hard&start_date=<today-7>`.
   Cross-check with `GET /stocks/{ts_code}/events?risk_level=hard` for coverage redundancy.
3. If any hit, fire a layer-0 SELL signal with `publish_time`, `risk_category`, `risk_level`,
   and source URL surfaced to the user — never silent-execute.

Match-by-name caveat (carried over from the partner blind-spot context):

- Some risk events do not populate `raw_ts_code` and only carry the company name in the title.
  When the sell-rule skill filters by `ts_code` alone, it may miss those rows. Use the
  `stock_name` filter as the secondary lookup for each held position's display name.

## `/search`, `/stocks`, `/stocks/summary`, `/stocks/filters` Guide

Use these for browsing or filtering the stock universe before drilling into specific endpoints.

### Endpoint Choice

- `GET /search?q=<keyword>`: lightweight fuzzy search for stocks/market objects by code or name.
  Use as the first hop when the user provides a partial Chinese name.
- `GET /stocks`: paginated, filterable stock pool list. Supports keyword, board, watchlist scope,
  industry, tier, theme_code. Use when the user wants to browse a slice of the universe.
- `GET /stocks/summary`: aggregate up/down counts, limit-up/limit-down counts. Use as the
  high-level summary alongside `/stocks`.
- `GET /stocks/filters`: returns valid filter values (industries, tiers, themes). Use to validate
  or display filter options to the user before calling `/stocks`.

### Notes

- `/stocks` already integrates with the user's `/watchlist` — pass `scope=watchlist` (or similar
  filter, check `/stocks/filters` for the exact key) instead of joining manually.
- Amount fields are returned in 元 by default; do not re-convert from 万 unless `/stocks/summary`
  documents otherwise in its response.

## Toplist Seat Chain Guide (龙虎榜补充)

When the user asks about 游资 / 营业部席位 / 席位关联, supplement `/toplist` and
`/stocks/{ts_code}/toplist` with the seat-chain endpoints.

### Endpoint Choice

- `GET /stocks/{ts_code}/top-list-seat-chain`: linked broker-seat history across recent toplist
  appearances for the same stock. Use to trace which seats keep showing up together.
- `GET /stocks/{ts_code}/top-list-hot-money`: hot-money seat candidates for a given trade_date /
  operating department. Use when the user names a department.
- `GET /stocks/{ts_code}/top-list-hot-money-buyers`: buyer-side hot-money lineup for the stock.
  Use when the user asks 「谁在买 / 哪些游资进场」.

### Interpretation Rules

- 同一席位连续出现 ≠ 同一游资,标注「同营业部席位」即可,不要做具体游资归属断言。
- 不要把 buyer side 与 seller side 混淆;`hot-money-buyers` 只覆盖买方席位。
