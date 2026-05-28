# StockPillar Industries And Events Reference

## `/industries/*` Guide

Use the industry endpoints when the user asks for:

- 行业 tier / agent 路由关系
- 某个交易日的行业估值基线
- 某个交易日的行业因子排名
- 某个交易日的行业上下文快照
- 某个交易日的行业事件标签

### Endpoint Choice

- `GET /industries/mappings`: static mapping from `industry_name` to `config_tier` and `agent_type`
- `GET /industries/status`: latest sync/runtime status for industry-related tables
- `GET /industries/valuation-metrics`: valuation baseline by industry and trade date
- `GET /industries/factors`: factor and final-score ranking by industry and trade date
- `GET /industries/context`: merged runtime context used by the industry layer
- `GET /industries/events`: event tags with pagination

### Required Parameters

- `trade_date` or `previous_trade_date=true` is required for:
  - `/industries/valuation-metrics`
  - `/industries/factors`
  - `/industries/context`
  - `/industries/events`
- `/industries/mappings` and `/industries/status` do not need `trade_date`

### Optional Filters

- `industry_name`: narrow the query to one industry such as `白酒`
- `agent_type`: narrow to an agent lane such as `consumer`, `tech`, `resource`, `finance`
- `page` and `size`: supported by all `/industries/*` endpoints

Encoding rule:

- do not hand-concatenate non-ASCII query values into a raw URL string
- let the HTTP client encode Chinese values such as `白酒`
- if using `curl`, prefer `-G --data-urlencode` for non-ASCII query params

### Response Notes

- Industry records already include `config_tier` and, where applicable, `agent_type`
- `/industries/status` is the best endpoint to distinguish "route works but data source is empty" from "route is missing"
- `/industries/mappings` is the best source when the user only asks how an industry is classified
- `/industries/events` returns paged event rows, total count, and `source_ready`
- `/industries/factors` and `/industries/context` return one record per industry for that trade date
- `/industries/valuation-metrics` returns both current median-style fields (`pe_ttm_median`, `pb_median`, `roe_median`) and compatibility aliases (`avg_pe`, `avg_pb`, `avg_roe`, `median_mv`, `avg_dividend_yield`, `avg_netprofit_yoy`)
- Pagination metadata for `/industries/*` is returned inside `data.page`, `data.size`, and `data.total`

### Response Differences And Normalization Rules

These response differences are expected. Normalize them explicitly instead of guessing.

- `/prices/realtime`
  - `pct_chg` may be absent
  - when absent, compute it as `(price - pre_close) / pre_close * 100`
  - `update_time` may be absent
  - when absent, use `trade_time` as the practical timestamp field

- `/screen/stocks`
  - the response typically returns `market_cap`
  - do not expect a returned `total_mv` field in the payload
  - `total_mv` is still a valid screening field, but response parsing should read `market_cap`
  - this is asymmetric by design: request filters may use `total_mv` or the alias `market_cap`, but the response should be read from `market_cap`

- `/industries/*`
  - list-like rows are usually under `data.records`
  - pagination metadata is under `data.page`, `data.size`, `data.total`, and often `data.count`
  - do not assume the list is a top-level raw array

- `/positions/trades`
  - rows are under `data.orders`
  - pagination metadata is under `data.page`, `data.size`, `data.total`, and `data.count`
  - the `summary` block aggregates the filtered execution records, not current holdings

- `/top20/daily`
  - there is no normal pagination shape
  - parse the Top20 list directly from the returned `data`
  - if `score_value` is absent or null, downstream parsing may need `raw_payload_json`

- `/industries/events`
  - always inspect `source_ready`
  - if `source_ready=false`, empty rows usually mean the upstream event pipeline is not ready, not that the endpoint is broken

- `notes`
  - some industry payloads may expose a `notes` field containing implementation detail
  - treat it as non-authoritative developer context, not as a trading signal
  - do not surface `notes` to end users unless they explicitly ask for backend or debug context

### Field Units And Ranges

These fields are easy to misread. Treat them with the following units:

- `price_momentum_5d` and `price_momentum_20d`: already expressed as percentage values, not decimal fractions. Example: `6.04` means `6.04%`, not `0.0604` and not `604%`.
- `valuation_percentile`: percentile-style score in the `0-100` range, not a raw valuation multiple.
- `base_score`, `event_score`, `trading_score`, and `final_score`: normalized scores in the `0-100` range, not returns.
- `pe_ttm_median`, `pb_median`, `roe_median`, `gpm_median`, `avg_pe`, `avg_pb`, `avg_roe`: raw metric values, not percentile scores.
- `avg_dividend_yield`: percentage-style value. Example: `1.8` means `1.8%`.
- `median_mv`: market-cap median in `万元`, not `亿元`.
- `total_mv`: market-cap field in `万元`, the same unit family as `median_mv`.
- `avg_netprofit_yoy`: percentage-style YoY growth value. Example: `15.3` means `15.3%`.
- `north_money_net_inflow` and `main_force_net_inflow`: amount fields from the stored industry tables. Do not reinterpret them as percentages.

`amount` context:

- In `/positions/trades`, `amount` means gross turnover before fees and is expressed in yuan.
- In the K-line source table used for liquidity checks, `amount` is stored in `万元` and converted to yuan before comparison.
- In `/moneyflow/hsgt/top10`, the comparable turnover field is `turnover_amount`, not the trade-order `amount` field.

### Agent Output Guidance

- Always state the trade date actually used.
- If you used `previous_trade_date=true`, say that the backend resolved the previous trading day automatically.
- Keep `config_tier` and `agent_type` distinct:
  - `config_tier` is the valuation/config grouping
  - `agent_type` is the runtime agent routing lane
- When comparing industries, prefer `/industries/factors` because it is already ordered by `final_score`.
- Do not convert industry momentum fields again. `price_momentum_5d=6.04` should be read and reported as `6.04%`.

## `/themes/{theme_code}/stock-pool` Guide

Use this when the user asks for the **committed, versioned theme research pool** rather than the
daily overlay-ranked picks. Typical phrasing:

- 主题股票池里有哪些股 / 当前 AI 主题的核心层是谁
- L1 核心层、L4 概念层各有哪些标的
- 半导体底座类（L1B）/ AI芯片 / 光模块 段的成分股
- 这个主题的池子是什么时候建的、上一版本是哪个
- 这只票是怎么被纳入主题池的（取 `level_reason` / `classification_reason` / `evidence_summary`）

### Endpoint Choice

- `GET /themes/{theme_code}/stock-pool`: snapshot rows of the current (or specified) version,
  with per-row layer, segment, core_type, operation suggestion, audit reasons. Backed by table
  `theme_stock_pool_snapshot`.
- `GET /themes/{theme_code}/stock-pool/versions`: the version timeline. Backed by
  `theme_pool_version`. Use when the user asks for version history or wants to diff versions.

Do **not** confuse this with:

- `GET /themes/{theme_code}/stocks` — overlay-day preferred basket, daily ranking (different table,
  different intent).
- `GET /themes/{theme_code}/market-stocks` — supply-chain-driven theme rows with price/funds rows.

### Parameters

- `source_version` (optional): explicit version key such as `V1.3` or `ai_full_chain_v1_4`.
  Default = current active version (`is_current=1`).
- `level_code` (optional): one of `L1`, `L2`, `L3`, `L4`, `L5`, `PRIMARY`, `INDEX`, `UNIVERSE`.
- `segment_code` (optional): supply-chain segment code such as `AI_CHIP`, `OPTICAL_CPO`, `PCB`,
  `MEMORY_ADV_PACKAGING`, `AIDC_POWER_COOLING`, `IDC_CLOUD`, `SEMI_BASE`, `AI_SOFTWARE`,
  `AI_APPLICATION`, `AIGC_CONTENT`, `ROBOTICS_EMBODIED`, `EDGE_AI_IOT`, `DATA_TOOLCHAIN`,
  `WEAK_CONCEPT`, `OTHER`. Filter narrows by exact match.
- `core_type` (optional): `L1A` (direct AI elasticity) or `L1B` (semiconductor base core).
- `page`, `size`: standard pagination; default `size=200`, max `1000`.
- `/versions` endpoint: optional `limit` (default 20, max 200).

### Response Shape

`/stock-pool` returns:

```json
{"version": {"source_version": "V1.3", "snapshot_date": "2026-05-27",
              "is_current": true, "build_status": "ACTIVE",
              "classifier_version": "rule_v1_3",
              "source_config_json": {...}},
 "records": [{"ts_code": "300308.SZ", "level_code": "L1", "segment_code": "OPTICAL_CPO",
              "core_type": "L1A", "operation_suggestion": "核心跟踪", ...}],
 "page": 1, "size": 200, "total": 47}
```

`source_detail_json` and `matched_rules_json` are returned as parsed JSON (not strings).

### Interpretation Rules

- The pool is **research-grade and versioned**, not a daily signal. State the version and
  snapshot date in the answer (`基于版本 V1.3 / 快照日 2026-05-27`).
- `level_code` represents committed conviction: L1 core, L2 important, L3 watch, L4 concept,
  L5 cut. Generic layers (`PRIMARY`, `INDEX`, `UNIVERSE`) come from the workbook-style imports.
- `core_type=L1B` only appears for semiconductor-base segments — do not treat it as a generic flag.
- `is_current=false` means the version was archived; do not call it the active pool.

## `/events/*` Guide

Use the event evidence endpoints when the user asks:

- 今天有哪些新闻事件
- 某个主题为什么加分或减分
- 某条新闻影响哪些个股、行业或主题
- 某只股票最近有哪些事件催化或风险
- 事件打分是否有效，后验表现如何

### Endpoint Choice

- `GET /events/raw`: raw normalized event feed from sources such as 财联社、东方财富、公告、个股新闻. Use this first when the user asks for source news, event stream, or raw evidence.
- `GET /themes/{theme_code}/overlay`: one-day theme overlay payload including `theme_core_score`, `theme_event_adjusted_score`, `theme_stance`, `theme_confidence`, `preferred_industries`, and `preferred_stock_pool`. Use this first when the user asks whether the theme is strengthening or weakening.
- `GET /themes/{theme_code}/stocks`: theme-scoped preferred stock pool. Use this when the user asks for the current AI theme basket, core beneficiaries, or representative names.
- `GET /themes/{theme_code}/daily-brief`: cached one-day theme analyst output. Use this first when the user asks for a theme summary, theme daily view, or wants to discuss the theme interactively. Do not force regeneration from this skill.
- `GET /themes/{theme_code}/market-pulse`: theme supply-chain stock pool market pulse. Use this when the user asks for theme-level funds, price movement, turnover, valuation, or which layer/branch is strongest.
- `GET /themes/{theme_code}/market-stocks`: theme-related stock rows with supply-chain reason plus price, funds, turnover, and valuation. Use this for ranking stocks inside a theme.
- `GET /themes/{theme_code}/market-history`: historical theme trend from `kline_daily`, `moneyflow`, and `valuation_data`. Use this when the user asks how the theme moved over a date range.
- `GET /themes/{theme_code}/events`: theme-level structured event tags joined with raw event title, summary, source, publish time, and URL. Use this when explaining theme impact.
- `GET /stocks/{ts_code}/events`: stock-level structured event tags joined with raw event evidence. Use this when explaining a stock-specific catalyst or risk. Rows include `risk_level` (`hard` / `soft` / `none`) and `risk_category`; pass `risk_level=hard` to fetch only hard-risk alerts.
- `GET /events/outcomes`: post-event market feedback. Use this when evaluating whether event scoring has been historically effective.

### Parameters

- `trade_date`: exact day in `YYYYMMDD`; the service expands it to the full day for raw/theme/stock event endpoints.
- `previous_trade_date=true`: use when the user asks for "上一个交易日".
- `stock_limit`: optional for `/themes/{theme_code}/overlay` and `/themes/{theme_code}/stocks`; defaults to backend ranking size.
- Theme daily-brief regeneration is a maintenance action. Do not add `force_refresh=true` from this skill.
- `start_time` and `end_time`: optional datetime range for raw/theme/stock event endpoints, format `YYYY-MM-DD HH:MM:SS`.
- `start_trade_date` and `end_trade_date`: optional date range for `/events/outcomes`, format `YYYYMMDD`.
- `page` and `size`: all four event endpoints support pagination. `size` may be up to 500.
- `ingest_source`: optional for `/events/raw`; common values are `cls_roll_list`, `eastmoney_kuaixun`, and `akshare`.
- `content_source_type`: optional for `/events/raw`; common values are `announcement`, `policy_news`, and `finance_news`.
- `event_type`: optional for theme and stock event tag endpoints.
- `sentiment`: optional for theme and stock event tag endpoints; common values are `positive`, `neutral`, and `negative`.
- `target_type`: optional for `/events/outcomes`; allowed values are `stock`, `industry`, and `theme`.
- `target_id`: optional for `/events/outcomes`; use `ts_code` for stock, industry name for industry, and theme code for theme.
- `outcome_label`: optional for `/events/outcomes`; common values are `positive`, `neutral`, and `negative`.

Do not combine:

- `trade_date` with `start_time` or `end_time` on `/events/raw`, `/themes/{theme_code}/events`, or `/stocks/{ts_code}/events`.
- `trade_date` with `start_trade_date` or `end_trade_date` on `/events/outcomes`.

### Important Fields

- Raw event rows include `id`, `ingest_source`, `content_source_type`, `content_source_name`, `publish_time`, `title`, `summary`, `content_text`, `url`, `raw_ts_code`, `raw_industry_hint`, and `raw_theme_hint`.
- Theme event rows include `theme_code`, `theme_name`, `event_type`, `sentiment`, `importance_score`, `impact_direction`, `impact_window`, `mapping_confidence`, plus raw event source fields.
- Theme overlay rows include `theme_core_score`, `theme_event_adjusted_score`, `theme_stance`, `theme_confidence`, `preferred_industries`, and `preferred_stock_pool`.
- Theme daily brief rows include `theme_status`, `primary_drivers`, `bullish_points`, `risk_points`, `representative_stocks`, `summary`, `analysis_version`, and `from_cache`.
- Stock event rows include `ts_code`, `stock_name`, `industry_name`, `theme_code`, `event_type`, `sentiment`, `importance_score`, `impact_direction`, `impact_window`, `mapping_confidence`, plus raw event source fields.
- Outcome rows include `event_id`, `target_type`, `target_id`, `trade_date`, `t1_return`, `t3_return`, `t5_return`, `t20_return`, `excess_return_t1`, `excess_return_t5`, `excess_return_t20`, `max_drawdown_t5`, `outcome_label`, and `outcome_score`.

### Interpretation Rules

- Treat `/events/raw` as evidence, not as scored impact. Raw events may not yet be mapped to stocks, industries, or themes.
- Treat `/themes/{theme_code}/daily-brief` as the preferred cached analyst conclusion for that date. Do not ask the agent to regenerate the same day from scratch; use the web maintenance path or scheduled pipeline for refreshes.
- When the user wants to discuss a theme conversationally, prefer the sequence `/themes/{theme_code}/daily-brief` -> `/themes/{theme_code}/overlay` -> `/themes/{theme_code}/events` rather than jumping straight to raw events.
- Treat `importance_score` as a rule-based current estimate, not a scientifically calibrated truth.
- Treat `mapping_confidence` as the confidence of the event-to-target mapping, not the expected return.
- Use `/events/outcomes` to check whether a class of events actually produced positive or negative market feedback.
- If `/events/outcomes` is empty, say there is no available post-event calibration data yet; do not conclude the event had no impact.
- When explaining impact, cite the source event `title`, `publish_time`, `content_source_name`, and URL if present.

## Theme Supplementary (主题补充)

When the basic theme overlay/events endpoints are not enough, these supplementary endpoints add
context for theme metadata, media coverage, supply-chain audit quality, and domestic-substitution
narratives.

### Endpoint Choice

- `GET /themes`: lists active themes. Use as the entry point when the user does not yet know which
  `theme_code` they want.
- `GET /themes/{theme_code}/news-videos`: AI-curated news video records for the theme on a
  given trade_date. Use when the user asks 「这个主题最近有什么新闻视频 / 媒体覆盖」.
- `GET /themes/{theme_code}/supply-chain/quality-audit`: graph quality audit findings —
  unreviewed candidates, low-confidence edges, dangling nodes. Use when the user asks
  「主题图谱信源是不是可靠 / 有没有低质量关系」. Read-only; mutation lives under the
  maintenance UI.
- `GET /themes/{theme_code}/supply-chain/domestic-substitution`: the domestic-substitution
  candidate pool with status, technology layer, A-share mapping. Use when the user discusses
  国产替代 narratives or asks for substitution-themed beneficiaries.
- `GET /themes/{theme_code}/supply-chain/source-matrix`: per-source priority matrix that drives
  supply-chain propagation. Use when the user asks「这个判断是从哪个信源出来的 / 信源权重」.

### Parameters

- `/themes`: no params; rows include `theme_code`, `theme_name`, `theme_group`, `priority`,
  `is_active`. Sorted by `priority` then `theme_code`.
- `/themes/{theme_code}/news-videos`: optional `trade_date`, `limit` (default 8, max 50).
- `/themes/{theme_code}/supply-chain/quality-audit`: optional `limit` (default 200).
- `/themes/{theme_code}/supply-chain/domestic-substitution`: optional `page`, `size` (default 50,
  max 200).
- `/themes/{theme_code}/supply-chain/source-matrix`: no params beyond `theme_code`.

### Interpretation Rules

- `quality-audit` findings are advisory — they tag potential issues, not confirmed bugs. Surface
  the audit reason verbatim instead of paraphrasing.
- `domestic-substitution` rows tagged `WORKBOOK_V2` or `PROFILE_*` are research-curated; do not
  treat them as official disclosures.
- When `source-matrix` shows a source with low priority weight, do not amplify a claim that
  relies primarily on that source — flag the weakness instead.
- `news-videos` is media coverage, not a fundamental signal — never use it alone to make
  a directional call.
