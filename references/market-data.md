# StockPillar Market Data Reference

## Agent Decision Shortcut

Follow this shortcut before reading endpoint details:

- "现在 / 当前 / 最新 / 实时行情 / 盘中价格" -> `/prices/realtime` for A-share, HK, and U.S. realtime quotes.
- "分钟线 / 分时K / 1分钟K线 / 1m bar" -> `/stocks/{ts_code}/prices/minute` for A-share, HK, and U.S. 1m minute bars.
- "个股主力资金 / 个股净流入 / 个股资金趋势" -> `/stocks/{ts_code}/moneyflow`.
- "北向资金 / 沪深港通资金流 / 外资今天买卖" -> `/moneyflow/hsgt` or `/moneyflow/hsgt/overview`.
- "北向持仓 / 港股通持股比例 / 外资持股量" -> `/stocks/{ts_code}/flows/hk-hold`.
- "融资融券 / 两融余额" -> `/margin/summary`, `/margin/detail`, or `/stocks/{ts_code}/margin`.
- "日度市场状态 / 今天适不适合开仓" -> `/market/summary` or `/market/summary/v2`.
- "盘中情绪 / 当前市场热度 / 追强环境" -> `/market/sentiment_pulse` or `/market/sentiment_pulse/v2`.
- "指数调仓 / 调入调出 / 指数样本调整 / 某股票被哪些指数调入调出" -> `/index-rebalance-items`.

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
- `GET /index-rebalance-items`: official index rebalance item rows; use for指数样本调入调出、按公告日/生效日/指数/股票查询调仓明细.

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
- For index rebalance rows, state `announce_date`, `effective_date`, `index_code/index_name`, and `direction`; `direction=in` means调入, `direction=out` means调出.

### `/index-rebalance-items`

Use when:

- the user asks for index rebalance details, 调入/调出, 指数样本调整, or official exchange index adjustment rows
- the user asks which indexes will add/remove a specific stock
- the user asks for all rows from a particular notice date or effective date

Optional params:

- `ts_code`: stock code, e.g. `301511.SZ`
- `index_code`: local index code, e.g. `399001`, `000016`
- `direction`: `in` or `out`
- `source_name`: official source name such as `国证指数`, `上海证券交易所`, `中证指数`
- `announce_date`: `YYYYMMDD`
- `effective_date`: `YYYYMMDD`
- `start_effective_date`, `end_effective_date`: date range for effective date
- `is_active`: omit for active rows; pass `all` only if the user asks for inactive rows too
- `page`, `size`

Response shape:

- `data.records`: rows from `index_rebalance_item`
- `data.page`, `data.size`, `data.total`

Row fields include:

- `source_name`, `source_url`, `notice_title`, `announce_date`
- `effective_date`
- `index_code`, `index_name`
- `direction`, `ts_code`, `stock_name`, `exchange`
- `change_count`, `confidence`, `extracted_status`, `notes`

Example:

```bash
curl "$STOCKPILLAR_API_URL/index-rebalance-items?announce_date=20260529&direction=out&size=100" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

## Endpoint Rules

### `/prices/realtime`

Use when:

- the user asks `现在`, `当前`, `最新`, `盘中`, or `实时行情`
- the user wants latest price, intraday change, bid/ask, or turnover
- the user asks for Hong Kong or U.S. stock realtime quotes supported by StockPillar's Futu OpenD integration

Do not use when:

- the user wants minute bars; use `/stocks/{ts_code}/prices/minute`
- the user wants historical daily走势 or daily K-line
- the user wants a technical signal event

Example user asks:

- `现在贵州茅台多少钱`
- `帮我看 600519.SH 的实时行情`
- `比较一下茅台和五粮液当前涨跌`
- `看一下腾讯控股和苹果现在多少钱`

Required params:

- `ts_codes`

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/prices/realtime?ts_codes=600519.SH,00700.HK,AAPL.US" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- always include the latest price and pct change
- if `pct_chg` is absent, compute it from `price` and `pre_close`
- use `trade_time` as the practical timestamp when `update_time` is absent
- for multiple securities, present them side by side
- for HK/US rows, expect `source=futu_opend`, `market`, and `futu_code`; `00700.HK` and `HK.00700` are both valid inputs for Tencent, and HK symbols are zero-padded to five digits
- do not use this endpoint to answer minute bars or daily K-line; use `/stocks/{ts_code}/prices/minute` for same-day 1m bars and `/stocks/{ts_code}/prices/kline` for historical daily K-line
- do not describe realtime data as end-of-day confirmed close

### `/stocks/{ts_code}/prices/minute`

Use when:

- the user asks for `分钟线`, `分时K`, `1分钟K线`, `1m bar`, or intraday minute bars for one stock
- the user wants same-day intraday OHLCV bars rather than a snapshot quote
- the user asks for HK/US minute bars supported by StockPillar's Futu OpenD integration

Do not use when:

- the user only wants current/latest price; use `/prices/realtime`
- the user wants daily K-line or a multi-day historical price window; use `/stocks/{ts_code}/prices/kline`

Example user asks:

- `给我 600519.SH 今天的 1 分钟线`
- `看一下腾讯控股 20260617 的分钟线`
- `AAPL.US 今天盘中 1m K 线`

Required params:

- path `ts_code`
- query `trade_date` in `YYYYMMDD`

Optional params:

- `freq`: only `1m`; omit it unless the user explicitly asks and still use `1m`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/00700.HK/prices/minute?trade_date=20260617&freq=1m" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- A-share same-day rows come from QMT cache and usually include `source=qmt_1m`
- HK/US rows come from Futu OpenD and include `source=futu_opend`, `market`, `futu_code`, and `freq=1m`
- rows are minute OHLCV bars with `trade_time`, `open`, `high`, `low`, `close`, `volume`, and `amount`
- an empty `data` list means no cached or provider-returned bars for that stock/date, not that the stock did not trade
- do not promise non-1m frequencies or historical minute bars from this route

### `/stocks/{ts_code}/prices/kline`

Use when:

- the user asks for historical daily K-line, 日线, K线, 走势, or a date-range price window
- the user asks for HK/US historical daily prices such as `00700.HK`, `HK.00700`, `AAPL.US`, or `US.AAPL`

Required params:

- path `ts_code`
- query `start_date` and `end_date` in `YYYYMMDD`

Optional params:

- `limit` for HK/US rows; use only when you need to cap the response

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/AAPL.US/prices/kline?start_date=20260101&end_date=20260131" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- HK/US daily rows are ODS raw daily bars with `freq=1d`, `market`, `currency`, `adjust=none`, and source such as `polygon_grouped`, `tushare_hk`, or `yahoo_hk`
- summarize the date range, row count, latest close, interval change, high, and low
- do not use this route for minute bars or realtime quotes

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
