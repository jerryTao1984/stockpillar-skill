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
- A-share financial endpoints read the A-share financial tables; U.S. `.US` endpoints read SEC-derived tables (`source=sec_companyfacts`). Hong Kong financial statements are not skill-visible.
- For U.S. `.US` rows, optional `period_type` can filter SEC-derived rows such as `ANNUAL` or `CUMULATIVE` when the user asks for annual vs cumulative periods.

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
- `AAPL.US 最新 SEC 财报摘要`
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

U.S. example:

```bash
curl "$STOCKPILLAR_API_URL/stocks/AAPL.US/financial?period=4&period_type=ANNUAL" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" | jq '.'
```

Response guidance:

- start with the reporting period
- list the 3 to 6 metrics most relevant to the question
- separate valuation from profitability and growth
- for U.S. `.US`, cite `source=sec_companyfacts` and distinguish `income`, `balancesheet`, `cashflow`, and `indicators` sections
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
