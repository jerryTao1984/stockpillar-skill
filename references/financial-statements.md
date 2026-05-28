# StockPillar Financial Statements Reference

## Financial Statement Period Rule

For these endpoints:

- `GET /stocks/{ts_code}/financial`
- `GET /stocks/{ts_code}/balancesheet`
- `GET /stocks/{ts_code}/cashflow`
- `GET /stocks/{ts_code}/income`
- `GET /stocks/{ts_code}/express`

Use these rules:

- `period=latest` means latest one record
- numeric `period` means latest N records
- invalid `period` returns `400`
- if the user does not ask for history, prefer `latest`

## Endpoint Rules

### `/stocks/{ts_code}/financial`

Use when:

- the user asks for ROE, PE, PB, margins, growth, debt ratio, or overall fundamentals
- the user wants a compact financial quality snapshot

Do not use when:

- the user wants a raw statement line item from balance sheet, cash flow, or income statement
- the user wants a technical chart answer

Example user asks:

- `贵州茅台最新财务指标怎么样`
- `这只股票的 ROE 和估值水平高吗`
- `帮我看一下基本面质量`

Required params:

- `ts_code`

Optional params:

- `period`

`period` accepts:

- `latest`
- integer-like string such as `1`, `2`, `4`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/financial?period=latest" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- start with the reporting period
- list the 3 to 6 metrics most relevant to the question
- separate valuation from profitability and growth
- if the user asks whether it is `高` or `低`, frame it as relative and data-based, not absolute judgment

### `/stocks/{ts_code}/balancesheet`

Use when:

- the user asks for raw balance sheet items
- the user wants assets, liabilities, equity, cash, debt, or related statement fields

Do not use when:

- the user wants a compact summary and `/financial` is sufficient
- the user asks for cash flow or income statement fields instead

Required params:

- `ts_code`

Optional params:

- `period`

`period` accepts:

- `latest`
- integer-like string such as `1`, `2`, `4`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/balancesheet?period=latest" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### `/stocks/{ts_code}/cashflow`

Use when:

- the user asks for operating, investing, or financing cash flow fields
- the user wants raw cash flow statement items

Do not use when:

- the user wants a compact summary and `/financial` is sufficient
- the user asks for balance sheet or income statement fields instead

Required params:

- `ts_code`

Optional params:

- `period`

`period` accepts:

- `latest`
- integer-like string such as `1`, `2`, `4`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/cashflow?period=latest" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### `/stocks/{ts_code}/income`

Use when:

- the user asks for revenue, profit, margin, expense, or other raw income statement items
- the user wants raw P&L fields

Do not use when:

- the user wants a compact summary and `/financial` is sufficient
- the user asks for balance sheet or cash flow fields instead

Required params:

- `ts_code`

Optional params:

- `period`

`period` accepts:

- `latest`
- integer-like string such as `1`, `2`, `4`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/income?period=latest" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

### `/stocks/{ts_code}/express`

Use when:

- the user asks for earnings express or performance express data
- the user wants latest quick-report style fields rather than full statements

Do not use when:

- the user wants a full financial statement
- the user wants technical or market data

Required params:

- `ts_code`

Optional params:

- `period`

`period` accepts:

- `latest`
- integer-like string such as `1`, `2`, `4`

Request:

```bash
curl "$STOCKPILLAR_API_URL/stocks/600519.SH/express?period=latest" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

## Ownership, Capital, Pledges (公司基本面补充)

These endpoints extend the raw statement endpoints with shareholder structure, capital actions,
and pledge risk. They are **per-stock** (path `ts_code`) and most accept `page`/`size`.

### Endpoint Choice

- `GET /stocks/{ts_code}/events/holder-trades`: major shareholder buy/sell records.
- `GET /stocks/{ts_code}/events/block-trades`: block-trade (大宗交易) records.
- `GET /stocks/{ts_code}/events/repurchases`: company share-repurchase records.
- `GET /stocks/{ts_code}/ownership/holder-numbers`: shareholder count history (concentration).
- `GET /stocks/{ts_code}/ownership/top10-holders`: top-10 shareholders by period.
- `GET /stocks/{ts_code}/ownership/top10-floatholders`: top-10 floating shareholders by period.
- `GET /stocks/{ts_code}/pledges/detail`: per-stake equity-pledge detail rows.
- `GET /stocks/{ts_code}/pledges/stat`: aggregate pledge ratio time series.
- `GET /stocks/{ts_code}/ownership/overview`: combined holder/pledge/repurchase compact view.
  Optional `recent_limit` (default 5) caps the recent-events tail.
- `GET /stocks/{ts_code}/capital-overview`: capital and trading overview (resource allocation,
  IPO/raise history, share structure).
- `GET /stocks/{ts_code}/governance-overview`: governance and regulatory compact view
  (董监高变动、违规、ST 风险).

### Trigger Phrases

- 减持 / 增持 → `/events/holder-trades`
- 大宗交易 → `/events/block-trades`
- 回购 / 注销 → `/events/repurchases`
- 股东户数 → `/ownership/holder-numbers`
- 十大股东 → `/ownership/top10-holders`; 十大流通股东 → `/ownership/top10-floatholders`
- 质押 → `/pledges/detail` (明细) or `/pledges/stat` (比例)
- 总体股东结构 → `/ownership/overview`
- 公司资本结构 → `/capital-overview`
- 公司治理 → `/governance-overview`

### Compact-Overview vs Raw Endpoints

`/*-overview` endpoints aggregate multiple raw tables into a single compact payload for chat use.
Prefer them when the user asks a wide question (「这家公司股东结构和质押情况怎样」). Fall back
to the per-table endpoints when the user wants raw rows or longer history.

### Interpretation Rules

- Pledge ratio above 50% of controlling-shareholder stake is a soft risk flag — surface it but
  do not call it a hard liquidation risk on its own.
- Repurchases announced ≠ executed; the response usually carries both planned and executed
  amounts — distinguish them explicitly.
- 股东户数 increasing usually means dilution of concentration (筹码分散), decreasing means
  concentration (筹码集中). Do not conflate with float change.
- Block-trade discounts/premiums can be signal, but cite the discount level rather than calling
  it "good" or "bad".

### See Also

For per-endpoint **field names**, **date-filter conventions** (`ann_date` vs `trade_date`), and
**response rendering guidance** (e.g. lead with `pledge_ratio`, group by `ann_date` snapshot),
read [reference-data.md](reference-data.md). This section covers the *why* and *how to interpret*;
reference-data.md covers the *what fields to ask for and how to render them*.
