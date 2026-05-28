# StockPillar Route Index

## Route Index

Use this as the authoritative one-to-one route index for `src/web/skill_api.py`.

- `GET /positions`: Auth `Bearer token`; required params `none`; use for current holdings, with optional `status` filter.
- `POST /positions`: Auth `Bearer token`; required params JSON `ts_code`, `qty`, `cost_price`; use to execute a buy and create or update a holding.
- `POST /positions/{position_id}/sell`: Auth `Bearer token`; required params path `position_id`; use to execute a full or partial sell.
- `GET /positions/trades`: Auth `Bearer token`; required params `none`; use for historical buy or sell execution review.
- `GET /positions/summary`: Auth `Bearer token`; required params `none`; use for portfolio-level PnL and cost summary.
- `POST /positions/refresh`: Auth `Bearer token`; required params `none`; use to force an on-demand holding refresh.
- `GET /stocks/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use for single-stock basic info with derived `tier`.
- `GET /stocks/batch`: Auth `Bearer token`; required params `ts_codes`; use for batch basic info lookup.
- `GET /stocks/{ts_code}/prices/kline`: Auth `Bearer token`; required params path `ts_code`, `start_date`, `end_date`; use for a single-stock K-line window.
- `GET /prices/realtime`: Auth `Bearer token`; required params `ts_codes`; use for one or more realtime quotes.
- `GET /stocks/{ts_code}/technical/indicators`: Auth `Bearer token`; required params path `ts_code`; use for numeric indicator values such as MA, MACD, RSI, KDJ, and BOLL.
- `GET /stocks/{ts_code}/technical/alerts`: Auth `Bearer token`; required params path `ts_code`; use for single-stock signal events such as crossovers or oversold alerts.
- `GET /stocks/{ts_code}/technical/factor-pro`: Auth `Bearer token`; required params path `ts_code`; use for stock technical factor pro rows by trade date or date range.
- `GET /indices/{ts_code}/technical/factor-pro`: Auth `Bearer token`; required params path `ts_code`; use for index technical factor pro rows by trade date or date range.
- `GET /stocks/{ts_code}/prices/limits`: Auth `Bearer token`; required params path `ts_code`; use for daily up-limit and down-limit price records.
- `GET /stocks/{ts_code}/events/suspend`: Auth `Bearer token`; required params path `ts_code`; use for stock suspension and resumption records.
- `GET /stocks/{ts_code}/flows/hk-hold`: Auth `Bearer token`; required params path `ts_code`; use for stock-level northbound or southbound holding records.
- `GET /stocks/{ts_code}/events/share-float`: Auth `Bearer token`; required params path `ts_code`; use for restricted-share unlock records.
- `GET /stocks/{ts_code}/technical/cyq-perf`: Auth `Bearer token`; required params path `ts_code`; use for chip distribution reference metrics.
- `GET /stocks/{ts_code}/technical/cyq-chips`: Auth `Bearer token`; required params path `ts_code`; use for daily chip distribution price buckets.
- `GET /stocks/{ts_code}/events/limit-list`: Auth `Bearer token`; required params path `ts_code`; use for limit-up or limit-down board list records.
- `GET /stocks/{ts_code}/events/surveys`: Auth `Bearer token`; required params path `ts_code`; use for investor-relation and institution survey records.
- `GET /stocks/{ts_code}/flows/slb-sec-detail`: Auth `Bearer token`; required params path `ts_code`; use for securities lending detail records.
- `GET /concepts/{ts_code}/moneyflow/ths`: Auth `Bearer token`; required params path `ts_code`; use for THS concept moneyflow records.
- `GET /technical/radar`: Auth `Bearer token`; required params `none`; use for a market-wide technical scan.
- `GET /stocks/{ts_code}/moneyflow`: Auth `Bearer token`; required params path `ts_code`, `start_date`, `end_date`; optional params `page`, `size`; use for single-stock moneyflow history.
- `GET /moneyflow/hsgt`: Auth `Bearer token`; required params `start_date`, `end_date`; use for a multi-day northbound or southbound flow window.
- `GET /moneyflow/hsgt/overview`: Auth `Bearer token`; required params `none`; optional `trade_date`; when omitted, the backend resolves the latest available trading day; use for a one-day northbound overview with separate 沪/深 breakdown and Top10 activity.
- `GET /moneyflow/hsgt/top10`: Auth `Bearer token`; required params `none`; use for HSGT top active stocks by date, market, or stock filter.
- `GET /margin/summary`: Auth `Bearer token`; required params `none`; use for an exchange-level margin snapshot or date range.
- `GET /margin/detail`: Auth `Bearer token`; required params `none`; use for stock-level margin detail rows.
- `GET /stocks/{ts_code}/margin`: Auth `Bearer token`; required params path `ts_code`; use for canonical single-stock margin detail.
- `GET /stocks/{ts_code}/financial`: Auth `Bearer token`; required params path `ts_code`; use for a compact financial metrics snapshot.
- `GET /toplist`: Auth `Bearer token`; required params `none`; use for a market-wide toplist snapshot or one-day list.
- `GET /stocks/{ts_code}/toplist`: Auth `Bearer token`; required params path `ts_code`; use for one stock's toplist records.
- `GET /top20/daily`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for a daily score or prediction Top20 snapshot.
- `GET /industries/mappings`: Auth `Bearer token`; required params `none`; use for the industry-to-tier and agent routing map.
- `GET /industries/status`: Auth `Bearer token`; required params `none`; use for industry pipeline freshness and counts.
- `GET /industries/valuation-metrics`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry valuation baselines.
- `GET /industries/factors`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry factor ranking.
- `GET /industries/context`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for merged industry runtime context.
- `GET /industries/events`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry event tags with pagination.
- `GET /events/raw`: Auth `Bearer token`; required params `none`; use for原始新闻事件流 evidence, with optional time/source/type filters.
- `GET /themes/{theme_code}/overlay`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for theme overlay scores, stance, preferred industries, and preferred stock pool.
- `GET /themes/{theme_code}/stocks`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for the filtered theme stock pool already ranked by overlay priority.
- `GET /themes/{theme_code}/stock-pool`: Auth `Bearer token`; required params path `theme_code`; optional query `source_version` (default = current active version), `level_code` (`L1`-`L5`/`PRIMARY`/`INDEX`/`UNIVERSE`), `segment_code` (e.g. `AI_CHIP`, `OPTICAL_CPO`, `PCB`), `core_type` (`L1A`/`L1B`), `page`, `size`; use for the versioned A-share theme stock pool persisted in `theme_stock_pool_snapshot` (per-stock layer, segment, core_type, operation suggestion, evidence). Response payload is `{"version": {...}, "records": [...]}` with `page`/`size`/`total` reflecting filtered snapshot rows. Prefer this over `/themes/{theme_code}/stocks` when the user wants the committed multi-version research pool rather than the overlay-ranked daily picks.
- `GET /themes/{theme_code}/stock-pool/versions`: Auth `Bearer token`; required params path `theme_code`; optional query `limit` (default 20, max 200); use to list historical pool versions in `theme_pool_version` ordered by `snapshot_date` descending. Each row carries `source_version`, `parent_source_version`, `snapshot_date`, `classifier_version`, `build_status`, `is_current`, and parsed `source_config_json`.
- `GET /themes/{theme_code}/daily-brief`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for cached daily theme analysis. Do not pass `force_refresh=true` from this skill.
- `GET /themes/{theme_code}/market-pulse`: Auth `Bearer token`; required params path `theme_code`; optional query `trade_date`, `group_by`, `market`, `chain_code`, `layer_index`, `exposure_type`, `min_exposure_score`, `top_n`; use for theme-level price, turnover, main moneyflow, and valuation aggregation by supply-chain grouping.
- `GET /themes/{theme_code}/market-stocks`: Auth `Bearer token`; required params path `theme_code`; optional query `trade_date`, `market`, `chain_code`, `layer_index`, `exposure_type`, `min_exposure_score`, `sort_by`, `sort_order`, `page`, `size`; use for theme-related stock rows with supply-chain reason, price move, funds, turnover, and valuation.
- `GET /themes/{theme_code}/market-history`: Auth `Bearer token`; required params path `theme_code`, `start_date`, `end_date`; optional query `group_by`, `market`, `chain_code`, `layer_index`, `exposure_type`, `min_exposure_score`; use for historical theme price, funds, turnover, and valuation trends from `kline_daily`, `moneyflow`, and `valuation_data`. Date range is capped at 370 calendar days.
- `GET /themes/{theme_code}/events`: Auth `Bearer token`; required params path `theme_code`; use for主题事件标签 and raw evidence joined by event id.
- `GET /themes/{theme_code}/supply-chain/graph`: Auth not required; required params path `theme_code`; use for a theme's layered global supply-chain graph, including nodes, approved edges, layers, and company exposure edges.
- `GET /themes/{theme_code}/supply-chain/candidates`: Auth not required; required params path `theme_code`; use for AI-extracted supply-chain candidate relations awaiting or after review. Rows include resolved node names and company/security display fields when a candidate has matched nodes. `system_rejected:*` reviewer notes mean the backend pre-check decided the relation should not enter the long-term graph.
- `GET /themes/{theme_code}/supply-chain/exposures`: Auth not required; required params path `theme_code`; optional query `chain_code`, `segment_node_id`, `company_node_id`, `review_status`; use for the reviewed company exposure pool that maps supply-chain segments/products/technologies to companies. Returns `records`; rows are resolved with segment/company names and securities such as `ts_code`, `stock_name`, `market`, and `is_a_share`. If the stored exposure table is empty, the endpoint can return read-only derived rows with `needs_sync=true`.
- `GET /themes/{theme_code}/supply-chain/a-share-candidates/search`: Auth not required; required params path `theme_code`, query `query`; optional query `top_k`, `min_score`; use to map a newly discovered supply-chain company or text to TopK A-share candidates from the Chroma vector index. Returns `records` with `ts_code`, `stock_name`, `vector_score`, `name_match_score`, `final_score`, and `match_reasons`. This endpoint is read-only and does not write graph data.
- `GET /themes/{theme_code}/supply-chain/prefilter-events`: Auth `Bearer token`; required params path `theme_code`; use for the high-relevance event funnel before supply-chain relation extraction.
- `GET /themes/{theme_code}/supply-chain/impacts`: Auth `Bearer token`; required params path `theme_code`; optional query `trade_date`, `start_time`, `end_time`, `page`, `size`; use for theme/date-level persisted supply-chain propagation summaries. Prefer this over looping through `/events/{event_id}/supply-chain-impact` when the user asks for today's AI supply-chain impact, daily impacted companies, or coverage status. Response includes `coverage`, event-level `records`, `impact_on_a_shares`, and `impact_on_securities`.
- `GET /stocks/{ts_code}/events`: Auth `Bearer token`; required params path `ts_code`; optional query `risk_level`, `risk_category`, `event_type`, `sentiment`, `trade_date`, `previous_trade_date`, `start_time`, `end_time`, `page`, `size`; use for个股事件标签 and raw evidence joined by event id. Rows include `risk_level` and `risk_category`; use `risk_level=hard` for hard-risk alerts.
- `GET /stocks/{ts_code}/supply-chain`: Auth `Bearer token`; required params path `ts_code`; use for a stock/company's supply-chain position and upstream/downstream relations.
- `GET /events/outcomes`: Auth `Bearer token`; required params `none`; use for事件后验市场表现 and score calibration evidence.
- `GET /events/{event_id}/supply-chain-impact`: Auth `Bearer token`; required params path `event_id`; use for persisted supply-chain impact propagation results from one event to companies/securities. Prefer `impact_on_a_shares` for A-share output. Security resolution can include direct company hits, direct segment exposures, and related same-chain segment exposures.
- `GET /macro`: Auth `Bearer token`; required params `start_date`, `end_date`; use for a date-ranged macro dataset.
- `POST /screen/stocks`: Auth `Bearer token`; required params JSON `filters`; use for structured stock screening and ranking.
- `GET /market/summary`: Auth `Bearer token`; required params `none`; use for an agent-friendly daily market state payload with subscores, risk flags, and guidance.
- `GET /market/sentiment_pulse`: Auth `Bearer token`; required params `none`; use for an agent-friendly intraday market state payload with subscores, risk flags, and guidance.
- `GET /market/summary/v2`: Auth `Bearer token`; required params `none`; use for the same v2 daily market state payload exposed through the explicit versioned path.
- `GET /market/sentiment_pulse/v2`: Auth `Bearer token`; required params `none`; use for the same v2 intraday market state payload exposed through the explicit versioned path.
- `POST /stocks/{ts_code}/analysis/report`: Auth `Bearer token`; required params path `ts_code`; use to generate an AI valuation report and shareable HTML.
- `GET /stocks/{ts_code}/balancesheet`: Auth `Bearer token`; required params path `ts_code`; use for raw balance-sheet statement rows.
- `GET /stocks/{ts_code}/cashflow`: Auth `Bearer token`; required params path `ts_code`; use for raw cash-flow statement rows.
- `GET /stocks/{ts_code}/income`: Auth `Bearer token`; required params path `ts_code`; use for raw income-statement rows.
- `GET /stocks/{ts_code}/express`: Auth `Bearer token`; required params path `ts_code`; use for earnings-express rows.
- `GET /health`: Auth `No auth`; required params `none`; use only for a lightweight service liveness check.

### Watchlist (User Self-Selected Pool)

- `GET /watchlist`: Auth `Bearer token`; required params `none`; use to list the token-owner's watchlist stocks. The user_id is resolved from token.
- `POST /watchlist/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use to add a stock to the token-owner's watchlist. Idempotent.
- `DELETE /watchlist/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use to remove a stock from the watchlist. Mutation but scoped to the caller's own pool — does **not** require the same confirmation flow as portfolio trades.

### Stock Listing and Search

- `GET /search`: Auth `Bearer token`; required params `q`; optional `limit` (default 8); use for lightweight name/code fuzzy search across stocks and market objects.
- `GET /stocks`: Auth `Bearer token`; required params `none`; optional filters: keyword, board, watchlist scope, industry_name, tier, theme_code, plus `page`/`size`; use for the filterable stock pool list.
- `GET /stocks/summary`: Auth `Bearer token`; required params `none`; use for aggregate up/down counts and limit-up/limit-down summary across the filtered pool.
- `GET /stocks/filters`: Auth `Bearer token`; required params `none`; use to fetch available filter options (industries, tiers, themes) for the stock listing UI.

### Stock-Level Capital, Ownership, Pledges

- `GET /stocks/{ts_code}/events/holder-trades`: Auth `Bearer token`; required params path `ts_code`; optional `page`/`size`; use for major shareholder buy/sell records.
- `GET /stocks/{ts_code}/events/block-trades`: Auth `Bearer token`; required params path `ts_code`; optional `page`/`size`; use for block-trade records.
- `GET /stocks/{ts_code}/events/repurchases`: Auth `Bearer token`; required params path `ts_code`; optional `page`/`size`; use for share-repurchase records.
- `GET /stocks/{ts_code}/ownership/holder-numbers`: Auth `Bearer token`; required params path `ts_code`; use for shareholder count history (concentration shifts).
- `GET /stocks/{ts_code}/ownership/top10-holders`: Auth `Bearer token`; required params path `ts_code`; use for the top-10 shareholders by period.
- `GET /stocks/{ts_code}/ownership/top10-floatholders`: Auth `Bearer token`; required params path `ts_code`; use for the top-10 floating shareholders by period.
- `GET /stocks/{ts_code}/pledges/detail`: Auth `Bearer token`; required params path `ts_code`; use for per-stake equity-pledge detail rows.
- `GET /stocks/{ts_code}/pledges/stat`: Auth `Bearer token`; required params path `ts_code`; use for aggregate pledge ratio time series.
- `GET /stocks/{ts_code}/ownership/overview`: Auth `Bearer token`; required params path `ts_code`; optional `recent_limit` (default 5); use for a combined holder/pledge/repurchase compact overview.
- `GET /stocks/{ts_code}/capital-overview`: Auth `Bearer token`; required params path `ts_code`; use for an agent-friendly capital/trading overview compact view.
- `GET /stocks/{ts_code}/governance-overview`: Auth `Bearer token`; required params path `ts_code`; use for an agent-friendly governance/regulation overview compact view.

### Toplist Seat Chain (龙虎榜补充)

- `GET /stocks/{ts_code}/top-list-seat-chain`: Auth `Bearer token`; required params path `ts_code`; use for the linked broker-seat history across recent toplist appearances.
- `GET /stocks/{ts_code}/top-list-hot-money`: Auth `Bearer token`; required params path `ts_code`; optional `trade_date`, `operate_dept_name`; use for hot-money seat candidates on a given day.
- `GET /stocks/{ts_code}/top-list-hot-money-buyers`: Auth `Bearer token`; required params path `ts_code`; use for the buyer-side hot-money lineup.

### Theme Supplementary

- `GET /themes`: Auth `Bearer token`; required params `none`; use to list active themes with `theme_code`, `theme_name`, `theme_group`, `priority`. The default browsing entrypoint when the user does not yet know which theme to focus on.
- `GET /themes/{theme_code}/news-videos`: Auth `Bearer token`; required params path `theme_code`; optional `trade_date`, `limit` (default 8, max 50); use for AI-curated theme-related news video records.
- `GET /themes/{theme_code}/supply-chain/quality-audit`: Auth `Bearer token`; required params path `theme_code`; optional `limit` (default 200); use for the supply-chain graph quality audit findings (unreviewed candidates, low-confidence edges, etc).
- `GET /themes/{theme_code}/supply-chain/domestic-substitution`: Auth `Bearer token`; required params path `theme_code`; optional `page`/`size` (default 50, max 200); use for the domestic-substitution candidate pool.
- `GET /themes/{theme_code}/supply-chain/source-matrix`: Auth `Bearer token`; required params path `theme_code`; use for the per-source priority matrix that drives supply-chain propagation weighting.

### Market Regime and Risk Events

- `GET /market/regime_events`: Auth `Bearer token`; required params `none`; optional `trade_date`, `risk_level`, `risk_domain`, `limit` (default 50), `offset` (default 0); use for market-regime-shift risk evidence. **Critical for sell-rule layer 0 / risk overlays**.
- `GET /risk-events/market`: Auth `Bearer token`; required params `none`; optional `start_date`, `end_date`, `risk_level`, `risk_domain`, `page`, `size` (default 50); use for the general market-level risk event feed sorted by publish time desc. Use alongside `/market/regime_events` for full risk coverage.
- `GET /risk-events/stocks`: Auth `Bearer token`; required params `none`; optional `start_date`, `end_date`, `ts_code`, `stock_name`, `risk_level`, `risk_category`, `page`, `size` (default 50); use for per-stock risk event feed (regulatory, delisting, fraud, hard risk). When asking about a specific stock, prefer this with `ts_code` filter — it covers risks beyond `/stocks/{ts_code}/events`.

### Valuation Aggregate

- `GET /valuation`: Auth `Bearer token`; required params `none`; optional `industry`, `tab` (default `all`), `limit` (default 30), `page`; use for the cached valuation report list / leaderboard. Paginated via `records`/`page`/`size`/`total`.
- `GET /valuation/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use for the cached AI valuation detail snapshot (already-generated report; does **not** trigger regeneration). To force regenerate, use `POST /stocks/{ts_code}/analysis/report`.

### Research Meetings (调研/路演纪要)

- `GET /research-meetings`: Auth `Bearer token` scope `research_meeting:read`; required params `none`; optional `limit` (default 100); use to list research meetings in newest-first order.
- `GET /research-meetings/{meeting_id}`: Auth `Bearer token` scope `research_meeting:read`; required params path `meeting_id`; use for meeting detail with latest analysis, candidate events, and evidence segments.
- `GET /research-meetings/candidates`: Auth `Bearer token` scope `research_meeting:read`; required params `none`; optional `meeting_id` (filter to one meeting); use for the candidate-event review queue across meetings.
- `GET /research-meetings/{meeting_id}/candidates`: Auth `Bearer token` scope `research_meeting:read`; required params path `meeting_id`; optional `review_status`, `limit` (default 200); use for candidate events tied to one meeting.
- `POST /research-meetings/import`: Auth `Bearer token` scope `research_meeting:import`; required params JSON `meeting metadata payload`; **requires explicit user confirmation** because it ingests external ASR/recording data into the corpus.
- `POST /research-meetings/{meeting_id}/segments/batch`: Auth `Bearer token` scope `research_meeting:write_segment`; required params path `meeting_id`, JSON `segments`; **requires explicit user confirmation**; use to upsert ASR transcript segments batch by batch.
- `POST /research-meetings/{meeting_id}/analyze`: Auth `Bearer token` scope `research_meeting:analyze`; required params path `meeting_id`; **requires explicit user confirmation** since it triggers AI analysis and may incur model cost.
- `POST /research-meetings/candidates/{candidate_id}/review`: Auth `Bearer token` scope `research_meeting:review`; required params path `candidate_id`, JSON `reviewer`, `decision`; **requires explicit user confirmation**; on approval writes into `event_raw_feed`.
- `POST /research-meetings/candidates/auto-approve`: Auth `Bearer token` scope `research_meeting:review`; required params JSON profile config; **requires explicit user confirmation**; do **not** call without the user naming both the meeting and the auto-approve profile.

Route usage notes:

- `Required params` lists only hard requirements. Many read endpoints also accept optional filters such as `page`, `size`, `trade_date`, `start_date`, `end_date`, `period`, `refresh`, `industry_name`, and `agent_type`.
- Prefer the canonical stock-scoped path when the user is clearly asking about one stock.
- Prefer the market-wide path when the user asks for the latest list or a same-day board snapshot.
- In `actions[]`, `endpoint` must exactly match one route above.
- In `actions[]`, path placeholders go into `path_params`, URL query fields go into `query_params`, and JSON payload goes into `body`.
- Every `actions[]` item must include `purpose`.
- Do not invent endpoint paths, method names, or placeholder names.

## Conflict Resolution Rules

Use these rules before reading endpoint-specific details:

- Indicator values, numeric MA/MACD/RSI/KDJ/BOLL questions -> `GET /stocks/{ts_code}/technical/indicators`.
- One-stock signal detection such as gold cross, dead cross, overbought, oversold -> `GET /stocks/{ts_code}/technical/alerts`.
- Market-wide signal scan -> `GET /technical/radar`.
- Current/latest/intraday price -> `GET /prices/realtime`.
- Historical price structure or K-line window -> `GET /stocks/{ts_code}/prices/kline`.
- One-stock money movement -> `GET /stocks/{ts_code}/moneyflow`.
- Northbound/southbound aggregate money movement -> `GET /moneyflow/hsgt` or `/moneyflow/hsgt/overview`.
- Stock-level HSGT ownership or holding ratio -> `GET /stocks/{ts_code}/flows/hk-hold`.
- Daily market state -> `GET /market/summary` or `/market/summary/v2`.
- Intraday market mood -> `GET /market/sentiment_pulse` or `/market/sentiment_pulse/v2`.
- Supply-chain layer or graph structure -> `GET /themes/{theme_code}/supply-chain/graph`.
- Supply-chain segment to impacted companies -> `GET /themes/{theme_code}/supply-chain/exposures`.
- Theme price/funds/valuation pulse -> `GET /themes/{theme_code}/market-pulse`.
- Theme stock-level price/funds/valuation rows -> `GET /themes/{theme_code}/market-stocks`.
- Theme historical price/funds/valuation trend -> `GET /themes/{theme_code}/market-history`.
- Versioned committed theme A-share pool (multi-layer L1-L5, segment, core_type, audit) -> `GET /themes/{theme_code}/stock-pool` (+ `/versions` for history). Use this, not `/themes/{theme_code}/stocks`, when the user references the research-grade saved pool or asks for a specific version.
- Newly discovered company to A-share candidate mapping -> `GET /themes/{theme_code}/supply-chain/a-share-candidates/search`.
- One event's persisted propagation result -> `GET /events/{event_id}/supply-chain-impact`.

Mutation safety:

- `POST /positions` and `POST /positions/{position_id}/sell` require explicit user confirmation before calling.
- `POST /stocks/{ts_code}/analysis/report` is allowed only when the user explicitly asks to generate a report.
- `POST /research-meetings/import`, `POST /research-meetings/{meeting_id}/segments/batch`, `POST /research-meetings/{meeting_id}/analyze`, `POST /research-meetings/candidates/{candidate_id}/review`, `POST /research-meetings/candidates/auto-approve` are mutation endpoints — call only after explicit confirmation that covers the meeting id, the action, and (for review) the reviewer identity.
- Supply-chain maintenance, review, sync, extract, promote, disable, and propagation rerun actions are not routable from this skill; use the Web review/maintenance UI or scheduled pipeline.

**Forbidden from skill — do not call, even though the routes exist in the backend:**

- `POST /themes/{theme_code}/supply-chain/domestic-substitution/profiles/{profile_id}` — domestic substitution profile review/state update. Maintenance only.
- `POST /themes/{theme_code}/supply-chain/quality-audit/action` — applies a soft-cleanup action on quality audit findings. Maintenance only.
- `POST /themes/{theme_code}/supply-chain/impacts/rerun` — reruns supply-chain event propagation for a given event_id or date. Maintenance only.

If the user asks the skill to perform any of the above, decline and direct them to the supply-chain review/maintenance UI or the scheduled pipeline. Do not attempt to construct the path manually from the OpenAPI-style hints — these mutation endpoints are intentionally out of skill scope.
