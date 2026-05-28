---
name: StockPillar Stock Analysis Skill
description: Use this skill when the user asks about A-share stocks, technical indicators, market data, capital flow, financial metrics, stock screening, valuation-style reports, portfolio actions, industry/theme events, or AI supply-chain graph data from the StockPillar API.
author: StockPillar Team
version: "2.2.0"
requires:
  env:
    - STOCKPILLAR_API_KEY
    - STOCKPILLAR_API_URL
examples:
  - "查询贵州茅台的基本信息"
  - "查 600519.SH 最近 60 天的 MA、MACD、RSI、KDJ"
  - "今天有哪些股票出现了 MACD 金叉信号"
  - "筛选 ROE>15% 且 PE<20 的股票"
  - "生成贵州茅台的 AI 深度价值研报"
  - "查询上一个交易日的 score_top20"
  - "查询白酒行业的行业上下文和事件标签"
  - "查询 688256.SH 最近有哪些事件影响"
  - "查看 AI 主题供应链五层图谱"
  - "查询某条事件如何沿供应链传导到公司"
  - "买入 600519.SH 100 股，成本价 1500"
  - "查看最近 30 天的持仓交易流水"
tags:
  - stock
  - finance
  - a-share
  - technical-analysis
  - market-data
input_schema:
  type: object
  properties:
    actions:
      type: array
      description: Preferred multi-step execution plan. Each item maps to one StockPillar endpoint listed in references/route-index.md. Use this whenever the request needs more than one endpoint or any endpoint outside the legacy shortcut set.
      items:
        type: object
        properties:
          method:
            type: string
            enum: [GET, POST]
          endpoint:
            type: string
            description: API path such as /prices/realtime or /themes/{theme_code}/supply-chain/graph. Must exactly match one route in references/route-index.md; do not invent endpoints.
          path_params:
            type: object
            description: 'Values for endpoint placeholders, for example {"ts_code": "600519.SH"} for /stocks/{ts_code}.'
          query_params:
            type: object
            description: 'URL query parameters after normalization, for example {"start_date": "20260401", "end_date": "20260417", "indicators": "MA,MACD"}.'
          body:
            type: object
            description: JSON body for POST endpoints.
          purpose:
            type: string
            description: Short reason for this call in the analysis chain.
        required: [method, endpoint, purpose]
    query_type:
      type: string
      description: Legacy single-intent shortcut for the most common one-endpoint tasks. For anything not in the enum, use `actions[]` instead. Full natural-language → endpoint mapping lives in references/general-rules.md.
      enum:
        - basic_info
        - batch_query
        - realtime
        - kline
        - technical
        - technical_alerts
        - technical_radar
        - moneyflow
        - hsgt_overview
        - financial
        - screening
        - market_summary
        - market_pulse
        - top20_daily
        - positions
        - position_trades
        - position_summary
        - ai_report
    ts_code:
      type: string
      description: Single stock code such as 600519.SH.
    ts_codes:
      type: string
      description: Multiple stock codes joined by commas, max 100.
    start_date:
      type: string
      description: YYYYMMDD lower bound for time-ranged endpoints.
    end_date:
      type: string
      description: YYYYMMDD upper bound for time-ranged endpoints.
    trade_date:
      type: string
      description: YYYYMMDD for single-day snapshots.
    previous_trade_date:
      type: boolean
      description: Pass true for endpoints that support automatic previous-trading-day resolution (e.g. /top20/daily, /industries/*).
    indicators:
      type: string
      description: Comma-separated grouped indicator keys for /stocks/{ts_code}/technical/indicators. Allowed values are MA, EMA, MACD, RSI, KDJ, BOLL, VOL_MA, BIAS, CCI, WR. Do not pass leaf names like MA5 or RSI14.
    period:
      type: string
      description: latest or a positive integer string for financial-statement endpoints. Pass as a string, never an integer.
    filters:
      type: object
      description: 'Filter conditions for POST /screen/stocks. Each key is a supported numeric field or alias; each value is an operator object such as {"gt": 15}.'
    sort_by:
      type: string
      description: Optional sort field for /screen/stocks.
    sort_order:
      type: string
      enum: [asc, desc]
    limit:
      type: integer
      description: Optional row limit for /screen/stocks.
---

# StockPillar Skill

This skill defines the StockPillar API contract only. Strategy, position sizing, and portfolio
construction live in separate policy skills (e.g. dolphinagent, turtleagent). When both are loaded,
this one supplies endpoints and parameters; the policy skill supplies decisions.

This file is written for agents, not for human API consumers. Keep execution simple, deterministic,
and explicit.

## Input Mode

Prefer `actions[]` for any request that needs more than one endpoint, or any endpoint outside the
small `query_type` shortcut set. The `query_type` enum is intentionally narrow — the long-form
natural-language → endpoint mapping is in [references/general-rules.md](references/general-rules.md).

When constructing actions:

- `endpoint` must exactly match one route in [references/route-index.md](references/route-index.md).
- Put route placeholders in `path_params`.
- Put URL query string fields in `query_params`.
- Put JSON payload fields in `body`.
- Every action must include `purpose` so debugging can explain why the endpoint was called.

### Examples

Single intent — quick price lookup:

```json
{"actions": [
  {"method": "GET", "endpoint": "/prices/realtime",
   "query_params": {"ts_codes": "600519.SH"},
   "purpose": "查贵州茅台当前价"}
]}
```

Multi-intent research chain — price + technicals + funds + fundamentals:

```json
{"actions": [
  {"method": "GET", "endpoint": "/prices/realtime",
   "query_params": {"ts_codes": "600519.SH"},
   "purpose": "实时价位"},
  {"method": "GET", "endpoint": "/stocks/{ts_code}/technical/indicators",
   "path_params": {"ts_code": "600519.SH"},
   "query_params": {"start_date": "20260307", "end_date": "20260506",
                     "indicators": "MA,MACD,RSI,KDJ"},
   "purpose": "近 60 天技术指标"},
  {"method": "GET", "endpoint": "/stocks/{ts_code}/moneyflow",
   "path_params": {"ts_code": "600519.SH"},
   "query_params": {"start_date": "20260427", "end_date": "20260506"},
   "purpose": "近 10 天主力资金"},
  {"method": "GET", "endpoint": "/stocks/{ts_code}/financial",
   "path_params": {"ts_code": "600519.SH"},
   "query_params": {"period": "latest"},
   "purpose": "最新财务快照"}
]}
```

Event-to-stock supply-chain propagation:

```json
{"actions": [
  {"method": "GET", "endpoint": "/events/{event_id}/supply-chain-impact",
   "path_params": {"event_id": 12345},
   "purpose": "事件沿供应链对 A 股的传导结果"}
]}
```

Anti-pattern (do not do this): squeezing a multi-intent request into one `query_type=technical`
call and asking the model to free-form summarize. Use `actions[]` so each call is auditable.

## When To Use This Skill

Use this skill when the user asks for StockPillar data or actions, including:

- A-share stock basic info, realtime quotes, K-line, technical indicators, technical signals
- money flow, northbound/southbound flow, margin data, toplist, macro, market summary
- financial statements, valuation lists, AI-generated valuation reports
- industry runtime status, factors, context, events; theme overlays, theme events, stock events
- AI supply-chain graph, supply-chain company exposure, candidate review, event propagation
- daily Top20 lists, score/prediction archives, AI comments
- stock screening based on valuation, growth, or combined conditions
- portfolio holdings, PnL, buy/sell actions, trade-order review

Do not use this skill for U.S. stocks, crypto, options, or generic investing advice without
StockPillar data.

## Preconditions

Before calling the API:

1. Confirm `STOCKPILLAR_API_KEY` is present.
2. Read `STOCKPILLAR_API_URL` if set; otherwise default to
   `https://stockpillar.layercake18.com/api/skill/v1`.
3. Strip any trailing `/` from the base URL before joining with an endpoint path so the resulting
   request never contains `//api/skill/v1/...`. If you ever observe a double slash in a URL you
   built, normalize it before sending the request rather than retrying as-is.
4. Use a normal URL/HTTP client so query parameters are URL-encoded (especially Chinese values
   such as `industry_name=白酒`); never hand-build raw HTTP request lines.
5. Never hardcode real tokens into the skill or responses.

## Hard Safety Rules

- Prefer read-only endpoints first.
- Skill-visible writes are limited to portfolio actions.
- Trade endpoints (`POST /positions`, `POST /positions/{position_id}/sell`) require explicit user
  confirmation in the current conversation before execution. Confirmation must clearly cover the
  stock or position, side, quantity, and price or cost basis.
- Vague wording such as "买点", "卖点", "要不要上", "看着办", or "帮我操作" is **not** explicit
  confirmation. For vague trading intent, summarize the proposed order and ask for confirmation
  instead of calling the endpoint.

  Example flow:
  - User: "买点茅台吧"
  - Skill response: "需要确认：买入 600519.SH 多少股？以什么成本价？是否现在执行？"
- Read-only portfolio endpoints (`GET /positions`, `GET /positions/summary`,
  `GET /positions/trades`) do not require confirmation.
- Do not call supply-chain mutation, review, sync, extract, promote, disable, or propagation-rerun
  endpoints from this skill. Use the read-only supply-chain endpoints and direct users to the web
  review/maintenance UI or scheduled pipeline for changes.
- `POST /screen/stocks` is read-only screening despite using POST for JSON filters.

## Default Assumptions

- Default `theme_code` for AI theme, AI supply chain, AI event propagation, and AI company
  exposure queries is `AI_EMBODIED` unless the user names another theme.
- Supply-chain companies are not A-share-only. Global companies (NVIDIA, TSMC, OpenAI, etc.) can
  be valid upstream, downstream, competitor, or customer nodes.
- `flow` means money movement; `holding` means ownership/position. Do not confuse HSGT moneyflow
  with HSGT holding.

## Output Discipline

When answering with StockPillar data:

- State the stock code, theme code, event id, or endpoint scope used.
- State the date or date range used when the endpoint is time-bound.
- Distinguish facts from interpretation.
- Keep interpretation lightweight unless the user asked for analysis.
- Avoid definitive investment advice. Use phrasing like `仅基于当前接口数据`.

## Reference Modules

Load only the relevant module instead of reading everything:

- [references/route-index.md](references/route-index.md): authoritative one-to-one route index.
- [references/general-rules.md](references/general-rules.md): natural-language endpoint mapping,
  theme codes, parameter normalization, response contract, and common flags.
- [references/top20.md](references/top20.md): `/top20/daily` score and prediction list rules.
- [references/industries-events.md](references/industries-events.md): industry runtime, raw events,
  theme events, theme overlay, daily brief, stock events, event outcomes.
- [references/supply-chain.md](references/supply-chain.md): AI supply-chain graph, candidates,
  exposures, stock supply-chain position, event propagation.
- [references/positions.md](references/positions.md): holdings, buy/sell, trades, refresh, fees,
  trading-session, lot-size, T+1, liquidity-cap rules.
- [references/technical.md](references/technical.md): technical indicators, alerts, radar,
  K-line, screening.
- [references/market-data.md](references/market-data.md): realtime quotes, moneyflow, HSGT,
  margin, market supplements, market summary, intraday sentiment pulse.
- [references/financial-statements.md](references/financial-statements.md): financial summary,
  balance sheet, cashflow, income, express report, period rules.
- [references/reference-data.md](references/reference-data.md): per-endpoint deep reference for
  shareholder structure, holder trades, block trades, repurchases, pledges, and ownership overview
  — exact field names, date-filter conventions, and per-endpoint output guidance.
- [references/reports-macro-misc.md](references/reports-macro-misc.md): AI valuation reports,
  toplist, macro, health, request snippets, failure handling, response style.

## Core Execution Pattern

1. Identify the user's intent and endpoint family.
2. If the request has multiple intents, build `actions[]`; otherwise pick one endpoint or use a
   `query_type` shortcut.
3. Load only the relevant reference module.
4. Normalize stock code, theme code, event id, dates, and optional filters.
5. Apply the safety rules before any POST that mutates portfolio state.
6. Summarize the data in plain Chinese, with dates and metric names.

The shared response contract (`code` / `message` / `data` envelope, with `page` / `size` / `total`
merged into `data` when the endpoint paginates) is documented once in
[references/general-rules.md](references/general-rules.md#response-contract); do not duplicate it
here.
