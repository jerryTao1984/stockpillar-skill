---
name: stockpillar-skill
description: Use this skill when the user asks about A-share stocks, same-day A-share tick or call-auction replay, HK/US realtime quotes, HK/US historical K-line, U.S. SEC financials, technical indicators, market data, capital flow, shareholder structure, pledge or repurchase data, financial metrics, stock screening, valuation-style reports, portfolio actions, industry/theme events, versioned theme stock pools, or AI supply-chain graph data from the StockPillar API.
version: 2.4.0
metadata:
  openclaw:
    requires:
      env:
        - STOCKPILLAR_API_KEY
      bins:
        - curl
    primaryEnv: STOCKPILLAR_API_KEY
    envVars:
      - name: STOCKPILLAR_API_KEY
        required: true
        description: "StockPillar API token. Sent as the Authorization: Bearer header."
      - name: STOCKPILLAR_API_URL
        required: false
        description: API base URL. Defaults to https://stockpillar.layercake18.com/api/skill/v1
    emoji: "📈"
    homepage: https://stockpillar.layercake18.com
---

# StockPillar Skill

This skill defines the StockPillar API contract only. Strategy, position sizing, and portfolio
construction live in separate policy skills (e.g. dolphinagent, turtleagent). When both are loaded,
this one supplies endpoints and parameters; the policy skill supplies decisions.

This file is written for agents, not for human API consumers. Keep execution simple, deterministic,
and explicit.

## How To Call The API

StockPillar has no built-in tool. Make every request with `curl` through the shell.

1. Confirm `STOCKPILLAR_API_KEY` is set and non-empty before any call. If it is empty, stop and
   tell the user to configure it; do not invent a token.
2. Resolve the base URL: use `STOCKPILLAR_API_URL` if set, otherwise default to
   `https://stockpillar.layercake18.com/api/skill/v1`. Strip any trailing `/` before joining a path
   so the request never contains `//api/skill/v1/...`.
3. Use a real URL so query parameters are URL-encoded, especially Chinese values such as
   `industry_name=白酒`. Never hand-build raw HTTP request lines.

GET request:

```bash
curl -s -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/prices/realtime?ts_codes=600519.SH,00700.HK,AAPL.US"
```

POST request:

```bash
curl -s -X POST -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  -H "Content-Type: application/json" \
  "${STOCKPILLAR_API_URL:-https://stockpillar.layercake18.com/api/skill/v1}/screen/stocks" \
  -d '{"filters": {"roe": {"gt": 15}, "pe": {"lt": 20}}}'
```

For a multi-intent request (e.g. price + technicals + funds + fundamentals), send several `curl`
requests in sequence, one endpoint per call, and state the purpose of each call when you summarize.
Do not squeeze multiple intents into one endpoint and free-form guess the rest.

`endpoint` must exactly match a route in `references/route-index.md`. Do not invent endpoint paths,
method names, or placeholder names.

## When To Use This Skill

Use this skill when the user asks for StockPillar data or actions, including:

- A-share stock basic info, realtime quotes, same-day tick/call-auction replay, minute bars, K-line, technical indicators, technical signals
- HK/US realtime quotes, same-day 1m minute bars, and historical daily K-line
- U.S. SEC-derived financial summary, income statement, balance sheet, and cash flow
- money flow, northbound/southbound flow, margin data, toplist, macro, market summary
- financial statements, valuation lists, AI-generated valuation reports
- shareholder structure, top10 holders, holder count, pledge, repurchase, block trades
- industry runtime status, factors, context, events; theme overlays, theme events, stock events
- versioned theme stock pools, source versions, pool levels, and pool score/rank sorting
- AI supply-chain graph, supply-chain company exposure, candidate review, event propagation
- daily Top20 lists, score/prediction archives, AI comments
- stock screening based on valuation, growth, or combined conditions
- portfolio holdings, PnL, buy/sell actions, trade-order review

Do not use this skill for crypto, options, or generic investing advice without StockPillar data.
For U.S. and Hong Kong stocks, realtime quotes, same-day 1m minute bars, and historical daily K-line are skill-visible. U.S. stocks also have SEC-derived financial endpoints.

## Hard Safety Rules

- Prefer read-only endpoints first.
- Skill-visible writes are limited to portfolio actions and explicit watchlist add/remove actions.
- Trade endpoints (`POST /positions`, `POST /positions/{position_id}/sell`) require explicit user
  confirmation in the current conversation before execution. Confirmation must clearly cover the
  stock or position, side, quantity, and price or cost basis.
- Vague wording such as "买点", "卖点", "要不要上", "看着办", or "帮我操作" is **not** explicit
  confirmation. For vague trading intent, summarize the proposed order and ask for confirmation
  instead of calling the endpoint.

  Example flow:
  - User: "买点茅台吧"
  - Skill response: "需要确认：买入 600519.SH 多少股？以什么成本价？是否现在执行？"
- `POST /stocks/{ts_code}/analysis/report` is allowed only when the user explicitly asks to
  generate a report.
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

Reference files live in the `references/` directory next to this `SKILL.md`. Load only the module
relevant to the request instead of reading everything:

- [references/route-index.md](references/route-index.md): authoritative one-to-one route index.
- [references/general-rules.md](references/general-rules.md): natural-language endpoint mapping,
  theme codes, parameter normalization, response contract, and common flags.
- [references/top20.md](references/top20.md): `/top20/daily` score and prediction list rules.
- [references/industries-events.md](references/industries-events.md): industry runtime, raw events,
  theme events, theme overlay, daily brief, stock events, event outcomes.
- [references/theme-stock-pools.md](references/theme-stock-pools.md): versioned theme stock pools,
  source versions, level filters, and score/rank sorting.
- [references/supply-chain.md](references/supply-chain.md): AI supply-chain graph, candidates,
  exposures, stock supply-chain position, event propagation.
- [references/positions.md](references/positions.md): holdings, buy/sell, trades, refresh, fees,
  trading-session, lot-size, T+1, liquidity-cap rules.
- [references/technical.md](references/technical.md): technical indicators, alerts, radar,
  K-line, screening.
- [references/market-data.md](references/market-data.md): realtime quotes, moneyflow, HSGT,
  margin, market supplements, market summary, intraday sentiment pulse.
- [references/reference-data.md](references/reference-data.md): shareholder structure, top10
  holders, holder count, pledge, repurchase, block trades, holder trades, ownership overview.
- [references/financial-statements.md](references/financial-statements.md): financial summary,
  balance sheet, cashflow, income, express report, period rules.
- [references/reports-macro-misc.md](references/reports-macro-misc.md): AI valuation reports,
  toplist, macro, health, request snippets, failure handling, response style.

## Core Execution Pattern

1. Identify the user's intent and endpoint family.
2. Pick one endpoint per intent. Combine endpoints only when the user asked for mixed dimensions
   such as `价格 + 技术指标` or `技术信号 + 基本面`; then send the `curl` calls in sequence.
3. Load only the relevant reference module from `references/`.
   For versioned theme stock pool requests involving pool versions, levels, or score/rank sorting,
   load [references/theme-stock-pools.md](references/theme-stock-pools.md), not
   [references/industries-events.md](references/industries-events.md).
4. Normalize stock code, theme code, event id, dates, and optional filters per
   [references/general-rules.md](references/general-rules.md).
5. Apply the safety rules before any POST that mutates portfolio state.
6. Summarize the data in plain Chinese, with dates and metric names.

The shared response contract (`code` / `message` / `data` envelope, with `page` / `size` / `total`
merged into `data` when the endpoint paginates) is documented once in
[references/general-rules.md](references/general-rules.md#response-contract); do not duplicate it
here.
