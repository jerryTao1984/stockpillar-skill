# StockPillar Technical Reference

## Agent Decision Shortcut

Follow this shortcut before reading the detailed rules:

- User asks for indicator values or "MA/MACD/RSI/KDJ/BOLL 怎么样" -> `/stocks/{ts_code}/technical/indicators`.
- User asks "有没有金叉/死叉/超买/超卖/技术异动" for one stock -> `/stocks/{ts_code}/technical/alerts`.
- User asks "今天哪些股票出现信号/全市场扫描" -> `/technical/radar`.
- User asks for stored professional factor rows or explicitly says `factor_pro` -> `/stocks/{ts_code}/technical/factor-pro` or `/indices/{ts_code}/technical/factor-pro`.
- User asks for price走势, K线, 区间涨跌 -> `/stocks/{ts_code}/prices/kline`.
- User asks for conditional stock selection -> `/screen/stocks`.

## `/stocks/{ts_code}/technical/indicators` Guide

This is the most common source of agent mistakes. Follow the rules below strictly.

### When To Use `/stocks/{ts_code}/technical/indicators`

Use `GET /stocks/{ts_code}/technical/indicators` when the user asks for indicator values or indicator-derived interpretation, for example:

- `查一下贵州茅台的 MACD`
- `最近 60 天 RSI 怎么样`
- `给我看 MA 和 KDJ`
- `KDJ 和布林带现在是什么状态`
- `用技术指标判断是否超买超卖`

Important: this endpoint accepts grouped indicator keys, not arbitrary field names. Use `MA`, `EMA`, `MACD`, `RSI`, `KDJ`, `BOLL`, `VOL_MA`, `BIAS`, `CCI`, `WR`. Do not default to leaf names such as `MA5` or `RSI14` in the request unless backend support has been explicitly added.

Do not use `/technical/indicators` when the user is explicitly asking for signal events such as:

- `有没有 MACD 金叉`
- `今天是否出现死叉`
- `哪些股票超卖`
- `全市场扫描强势股`

Those should go to:

- `GET /technical/alerts` for one stock
- `GET /technical/radar` for market-wide scanning

### Required Parameters

Always send `indicators` for `/stocks/{ts_code}/technical/indicators`.

If `indicators` is omitted, the backend falls back to plain K-line fields rather than a default indicator set.

Date window behavior:

- if `start_date` and `end_date` are provided, use them directly
- if both are omitted, the backend defaults to the most recent 60 calendar days
- if only one boundary is provided, prefer filling the missing boundary explicitly rather than relying on implicit behavior

Recommended request pattern:

```bash
curl -G "$STOCKPILLAR_API_URL/stocks/600519.SH/technical/indicators" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "start_date=20260215" \
  --data-urlencode "end_date=20260416" \
  --data-urlencode "indicators=MA,MACD,RSI,KDJ"
```

### How To Choose the Date Range

Choose the smallest range that makes the indicators meaningful.

Recommended defaults:

- `当前 MACD / RSI / KDJ / BOLL`: last 60 calendar days.
- `短中长期均线`: use `/technical/indicators` with `MA`; use at least 300 calendar days if the user cares about `MA120` or `MA250`.
- `最近一周/一月/一季`: use the user-provided range directly.

Reason: many indicators need historical context. If the range is too short, the latest value may be incomplete or misleading.

### Indicator Selection Rules

If the user names indicators, use exactly those unless they clearly expect interpretive help.

Normalize user wording to grouped keys before calling the API:

- `MA5 / MA10 / MA20 / 均线` -> `MA`
- `EMA5 / EMA20 / 指数均线` -> `EMA`
- `RSI14 / RSI6 / RSI` -> `RSI`
- `KDJ / K / D / J` -> `KDJ`
- `布林带 / 上轨 / 下轨 / 中轨` -> `BOLL`
- `量能均线 / VOL_MA5` -> `VOL_MA`

If the user asks vaguely for `技术指标`, use a compact default set:

`MA,MACD,RSI,KDJ,BOLL`

If the user asks for trend:

`MA,MACD`

If the user asks for momentum:

`RSI,MACD,KDJ`

If the user asks for volatility or channel:

`BOLL`

### Common Indicators Cheatsheet

Use these grouped names in `indicators`:

- Moving averages: `MA`
- Exponential moving averages: `EMA`
- MACD family: `MACD`
- RSI family: `RSI`
- KDJ family: `KDJ`
- Bollinger family: `BOLL`
- Volume moving averages: `VOL_MA`
- Bias family: `BIAS`
- Other singles: `CCI`, `WR`

Allowed enum values for `indicators`:

`MA,EMA,MACD,RSI,KDJ,BOLL,VOL_MA,BIAS,CCI,WR`

The backend expands grouped names into concrete fields. For example:

- `MA` -> `MA5, MA10, MA20, MA60, MA120, MA250`
- `MACD` -> `MACD, MACD_Signal, MACD_Hist`
- `RSI` -> `RSI6, RSI12, RSI14, RSI24`
- `KDJ` -> `K, D, J`
- `BOLL` -> `BOLL_MID, BOLL_UP, BOLL_LOW, BOLL_WIDTH`

Do not invent custom group names.

### Request Key To Returned Fields

Use this as the authoritative enumeration for `/technical/indicators` requests:

- `MA`: `MA5, MA10, MA20, MA60, MA120, MA250`
- `EMA`: `EMA5, EMA10, EMA20`
- `MACD`: `MACD, MACD_Signal, MACD_Hist`
- `RSI`: `RSI6, RSI12, RSI14, RSI24`
- `KDJ`: `K, D, J`
- `BOLL`: `BOLL_MID, BOLL_UP, BOLL_LOW, BOLL_WIDTH`
- `VOL_MA`: `VOL_MA5, VOL_MA10, VOL_MA20`
- `BIAS`: `BIAS6, BIAS12`
- `CCI`: `CCI`
- `WR`: `WR`

Rules:

- `indicators` accepts only the request keys in the list above.
- The request should use grouped keys, not returned leaf fields.
- Example: if the user asks for `RSI14`, request `RSI`, then read `RSI14` from the response.
- Example: if the user asks for `MA20`, request `MA`, then read `MA20` from the response.

### Interpretation Rules

When the user asks for analysis rather than raw numbers:

1. Use the latest trading day in the response.
2. Report the indicator values first.
3. Then add a short interpretation.
4. Keep the interpretation directly tied to the returned data.

Examples:

- `RSI14 > 70`: can say `短线偏强，接近或处于超买区`
- `RSI14 < 30`: can say `短线偏弱，接近或处于超卖区`
- `MA5 > MA20`: can say `短线强于中期均线`
- `close > BOLL_UP`: can say `价格触及或突破布林上轨，波动放大`
- `MACD > 0` and rising: can say `动能偏强`

Do not claim `金叉` or `死叉` from one static row unless the data clearly shows a cross between recent periods. If the user specifically wants cross detection, prefer `/technical/alerts`.

### Minimal Answer Template

Use this shape for indicator questions:

```text
{name}（{ts_code}）截至 {latest_trade_date} 的技术指标如下：
- MA：MA5=...，MA20=...，MA60=...
- RSI14：...
- MACD：...
- KDJ：K=..., D=..., J=...

基于当前指标数据：
- 趋势：...
- 动能：...
- 风险提示：...
```

### Common Mistakes To Avoid

Avoid these errors:

- using `/technical/alerts` when the user asked for numeric indicator values
- using `/technical/indicators` when the user asked for a signal scan
- omitting `start_date` and `end_date`
- sending leaf names such as `MA5`, `RSI14`, or `K` instead of grouped keys
- inventing unsupported indicator names
- saying `金叉已形成` without cross-period evidence
- mixing `ts_code` and `ts_codes`

## Other Endpoint Rules

### `/stocks/{ts_code}/technical/alerts`

Use for one-stock signal detection such as:

- MACD gold cross / dead cross
- KDJ cross
- overbought / oversold
- breakout / breakdown

Good for: `今天贵州茅台有没有技术异动`

Do not use when:

- the user wants raw indicator values such as RSI14 or MA20
- the user wants a market-wide scan

Example user asks:

- `贵州茅台今天有没有技术异动`
- `600519.SH 是否出现 MACD 金叉`
- `这只股票现在有没有超买或超卖信号`

Required params:

- `ts_code`

Optional params:

- `trade_date`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/technical/alerts" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- first say whether any signal is present
- then list signal names and the latest relevant trade date
- then add one short interpretation tied to the returned signal
- do not fabricate the strength or duration of the signal

Signal object shape:

- each signal is an object with a `type` field
- RSI-derived signals use `type` + `value`
- MACD crossover signals use `type` + `diff`
- some signal types may carry no additional numeric field beyond `type`
- KDJ- and BOLL-style signal types should be treated as valid even when they only include `type`
- currently documented signal types include `RSI_OVERBOUGHT`, `RSI_OVERSOLD`, `MACD_GOLDEN_CROSS`, and `MACD_DEATH_CROSS`
- if the backend returns an unrecognized `type`, treat it as a valid signal and report it as-is rather than discarding it
- examples:
  - `{ "type": "RSI_OVERBOUGHT", "value": 82.1 }`
  - `{ "type": "RSI_OVERSOLD", "value": 24.7 }`
  - `{ "type": "MACD_GOLDEN_CROSS", "diff": 0.12 }`
  - `{ "type": "MACD_DEATH_CROSS", "diff": -0.08 }`

### `/technical/radar`

Use for market-wide scans such as:

- `今天哪些股票超卖`
- `扫描全市场 MACD 金叉`
- `找出当前强势突破的股票`

Do not use when:

- the user asks about one specific stock
- the user wants raw indicator values rather than scanned candidates

Example user asks:

- `今天有哪些股票出现了 MACD 金叉`
- `扫描全市场超卖股票`
- `找出当前强势突破的 A 股`

Required params:

- none

Optional params:

- `trade_date`

Request:

```bash
curl "$STOCKPILLAR_API_URL/technical/radar" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- the response is typically a plain list under `data`, not a paginated object
- each row usually includes `ts_code`, `trade_date`, `signals`, and `score`
- `signals` is a list of signal objects from the same detector family used by `/technical/alerts`, using `type` plus either `value` or `diff`
- see `/technical/alerts` above for signal object shape and the currently documented `type` values
- start with how many candidates were found by counting returned rows
- list the top candidates with stock code and signal type
- keep the explanation comparative and short
- make clear this is a scan result, not a full recommendation

### `/stocks/{ts_code}/technical/factor-pro` and `/indices/{ts_code}/technical/factor-pro`

Use these endpoints when the user asks for stored professional technical factors rather than grouped indicator expansion.

Choose the endpoint like this:

- `GET /stocks/{ts_code}/technical/factor-pro`: one stock's factor-pro rows
- `GET /indices/{ts_code}/technical/factor-pro`: one index's factor-pro rows

Use when:

- the user explicitly asks for `factor_pro`, `技术面专业因子`, or locally stored technical factor rows
- the task needs raw stored factor fields over a date range
- the user asks to compare stock factor-pro data with index factor-pro data

Do not use when:

- the user asks for common indicators such as MA, MACD, RSI, KDJ, or BOLL; use `/stocks/{ts_code}/technical/indicators`
- the user asks for signal events; use `/stocks/{ts_code}/technical/alerts` or `/technical/radar`
- the user asks for historical price走势 only; use `/stocks/{ts_code}/prices/kline`

Common params:

- `trade_date`: best for one-day lookup
- `start_date` + `end_date`: best for history or comparison
- `page`, `size`: supported for pagination

Request examples:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/technical/factor-pro?start_date=20260401&end_date=20260417" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

```bash
curl "$STOCKPILLAR_API_URL/indices/000001.SH/technical/factor-pro?trade_date=20260417" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- state whether the result is stock factor-pro or index factor-pro
- state the exact date or range used
- report only fields returned by the API; do not infer indicator values that are absent
- if the user did not explicitly ask for factor-pro, prefer the simpler indicator or K-line endpoints

### `/stocks/{ts_code}/prices/kline`

Use for historical走势 and price structure. If the user asks for `股价走势` or `K线`, do not substitute technical indicators unless they explicitly ask for them.

Use when:

- the user asks for recent走势, 区间涨跌, highest/lowest, or K-line data
- the user wants date-range price history
- the user asks for moving averages such as `MA5`, `MA20`, or `MA60` and backend MA fields are not explicitly verified

Do not use when:

- the user asks for realtime quote
- the user asks specifically for indicator values or signal detection

Example user asks:

- `看一下贵州茅台最近一个月走势`
- `给我 600519.SH 最近 30 天 K 线`
- `给我看 600519.SH 从 20260301 到 20260416 的价格表现`

Required params:

- `ts_code`
- `start_date`
- `end_date`

Optional params:

- `page`
- `size`

Notes:

- default to `page=1`
- use a larger `size` when you need a month or quarter window in one response

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/prices/kline?start_date=20260317&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- first give the date range
- then summarize latest close, interval change, high, and low
- if the user asked for moving averages, state they were derived from K-line closes
- mention volume or turnover only if it adds value
- if the user wants chart interpretation, say it is price-based rather than signal-based
- do not promise weekly or monthly aggregation unless the API has explicitly added those parameters

### `/screen/stocks`

Use for multi-condition stock selection. Keep filters structured and explicit. If the user gives natural language conditions, convert them into the narrowest valid JSON filter set.

Use when:

- the user gives screening conditions such as valuation, profitability, growth, momentum, or market cap
- the user wants a candidate list rather than one stock analysis

Do not use when:

- the user asks about one known stock
- the user asks for market summary instead of filtered securities

Example user asks:

- `筛选 ROE 大于 15%、PE 小于 20 的股票`
- `找一些低估值高成长的 A 股`
- `帮我按财务条件选股`

Supported numeric filter fields:

`close,pe_ttm,pe_static,pe_final,pb,dv_ttm,total_mv,roe,gpm,netprofit_yoy,peg,macd_hist,rsi6`

Supported aliases:

- `pe` -> `pe_final`
- `market_cap` -> `total_mv`
- `市值` -> `total_mv`

Unit note:

- `total_mv` is stored in `万元`
- `total_mv` uses the same `万元` unit family as `median_mv`
- example: `total_mv >= 50000` means at least 5 亿元
- adjust the range to match the user's intent; for example, `50000` to `500000` corresponds to about 5 亿 to 50 亿元

Recommended operators inside each filter object:

- `gt`
- `gte`
- `lt`
- `lte`
- `eq`

Contract for `filters`:

- `filters` must be a JSON object
- each key must be a supported numeric field or alias
- each value must be an operator object, not a raw scalar
- one field can contain one or more operators
- unsupported fields are ignored by the backend, so do not send guessed keys

Valid examples:

```json
{
  "filters": {
    "roe": { "gt": 15 },
    "pe": { "lt": 20 },
    "total_mv": { "gte": 50000, "lte": 500000 }
  }
}
```

Invalid examples:

```json
{
  "filters": {
    "roe_min": 15,
    "pe_max": 20,
    "industry": "消费"
  }
}
```

Do not assume free-text filters are supported. In particular, do not default to string filters such as `industry: "消费"` unless backend support for string matching has been added and verified.

Contract for sorting and paging:

- `sort_by` should use a supported numeric field or alias
- `sort_order` must be `asc` or `desc`
- if `sort_by` is invalid, the backend falls back to `total_mv`
- if `filters` is empty, the backend returns unscreened rows sorted by the requested sort field
- prefer setting `limit` explicitly; use `20` as the default agent choice unless the user asked for more

Request:

```bash
curl -X POST "$STOCKPILLAR_API_URL/screen/stocks" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "roe": {"gt": 15},
      "pe": {"lt": 20},
      "total_mv": {"gte": 50000, "lte": 500000}
    },
    "sort_by": "roe",
    "sort_order": "desc",
    "limit": 20
  }' | jq '.'
```

Response guidance:

- restate the applied filters in plain Chinese
- list the returned candidates with 2 to 4 key metrics
- do not claim the screen is exhaustive unless the API explicitly says so
- if the result set is large, summarize and show only the most relevant names
- avoid inventing filter keys like `roe_min` or `pe_max`; use operator objects such as `{"roe": {"gt": 15}}`
- prefer verified numeric fields over guessed text fields
- the API returns English keys such as `stock_code`, `stock_name`, `close`, `pe_ttm`, `roe`, `market_cap`, and `industry`
