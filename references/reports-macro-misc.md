# StockPillar Reports Macro And Misc Reference

## Endpoint Rules

### `/stocks/{ts_code}/analysis/report`

Use when:

- the user explicitly wants `研报`, `深度报告`, `价值分析`, or `AI 报告`
- the task needs a longer synthesized output instead of a quick factual reply

Do not use when:

- the user only asked a narrow factual question
- the user needs a fast quote or one metric

Example user asks:

- `生成贵州茅台的 AI 深度价值研报`
- `帮我出一份 600519.SH 的价值分析报告`

Required params:

- path param `ts_code`

Optional params:

- none

Request:

```bash
curl -X POST "$STOCKPILLAR_API_URL/stocks/600519.SH/analysis/report" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- tell the user a report was generated
- summarize the headline conclusion first
- then present the major sections in compact form unless the user wants the full text

### `/toplist`

Use when:

- the user asks about `今天龙虎榜有哪些股票`
- the user wants the latest market-wide toplist snapshot
- the user wants one trading day's toplist list rather than one stock's history

Do not use when:

- the user wants one stock's own toplist history

Optional params:

- `trade_date`
- `page`
- `size`

Request:

```bash
curl "$STOCKPILLAR_API_URL/toplist?trade_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- state whether the answer is latest-day or trade-date scoped
- summarize the leading entries first
- keep the summary descriptive, not predictive

### `/stocks/{ts_code}/toplist`

Use when:

- the user asks about 龙虎榜 candidates, unusual trading list entries, or a stock's toplist appearance
- the user wants a specific date's toplist or one stock's toplist records

Do not use when:

- the user wants broad market summary
- the user wants purely technical indicator values

Example user asks:

- `查一下 000001.SZ 最近有没有上龙虎榜`
- `查一下 600519.SH 在 20260416 有没有上龙虎榜`

Required params:

- path param `ts_code`

Optional params:

- `trade_date`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/toplist?trade_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- state whether the query is date-scoped or stock-scoped
- list the most relevant entries first
- keep the summary descriptive, not predictive
- each row may contain both `name` and `stock_name`; prefer `stock_name` when present

### `/macro`

Use when:

- the user asks for macroeconomic data from this API
- the user wants a date-ranged macro snapshot rather than stock-level analysis

Do not use when:

- the user wants one stock's fundamentals
- the user omits the date range and expects a specific macro window from the API

Example user asks:

- `查一下 20260101 到 20260416 的宏观数据`
- `给我一个最近一季度的宏观数据区间`

Required params:

- `start_date`
- `end_date`

Optional params:

- none

Request:

```bash
curl "$STOCKPILLAR_API_URL/macro?start_date=20260101&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- state the queried date range
- summarize the most important returned macro fields
- avoid inventing macro dimensions that are not in the response

### `/health`

Use when:

- the user asks whether the StockPillar API is alive
- you need a lightweight service availability check before a larger workflow

Do not use when:

- the user actually wants market or stock data

Request:

```bash
curl "$STOCKPILLAR_API_URL/health" | jq '.'
```

Response guidance:

- report whether the service responded normally
- do not treat health output as business data
## Request Snippets

### Basic Info

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### Realtime Quote

```bash
curl "$STOCKPILLAR_API_URL/prices/realtime?ts_codes=600519.SH" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### K-line

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/prices/kline?start_date=20260317&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### HSGT Moneyflow

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt?start_date=20260407&end_date=20260416" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### HSGT Overview

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt/overview?trade_date=20260417" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### HSGT Top10

```bash
curl "$STOCKPILLAR_API_URL/moneyflow/hsgt/top10?trade_date=20260417&market_type=1" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### Technical Alerts

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/technical/alerts" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### Technical Radar

```bash
curl "$STOCKPILLAR_API_URL/technical/radar" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

## Failure Handling

If the API returns an error:

- `400`: check code format, indicator names, missing dates, or invalid filters
- `401`: token missing or invalid
- `404`: security or dataset not found
- `429`: back off and retry with fewer requests
- `500`: tell the user the upstream service failed
- `502` or `503`: treat the upstream dependency as temporarily unavailable; report that clearly, retry only when appropriate, and fall back to any still-available partial result such as `score_top20`

When a request fails, report the concrete issue and, if possible, offer the closest valid retry.

## Response Style

Preferred answer style:

- concise summary first
- 3 to 6 high-signal bullets or short paragraphs
- date range explicit
- no long raw JSON dump unless the user asked for it

If the user asks for deep analysis, combine facts with a short interpretation section. If they ask for raw data, stay literal.
