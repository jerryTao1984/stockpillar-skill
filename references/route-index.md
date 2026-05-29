# StockPillar Route Index

## Route Index

Use this as the authoritative one-to-one route index for `src/web/skill_api.py`.

- `GET /positions`: Auth `Bearer token`; required params `none`; use for current holdings, with optional `status` filter.
- `POST /positions`: Auth `Bearer token`; required params JSON `ts_code`, `qty`, `cost_price`; use to execute a buy and create or update a holding.
- `POST /positions/{position_id}/sell`: Auth `Bearer token`; required params path `position_id`; use to execute a full or partial sell.
- `GET /positions/trades`: Auth `Bearer token`; required params `none`; use for historical buy or sell execution review.
- `GET /positions/summary`: Auth `Bearer token`; required params `none`; use for portfolio-level PnL and cost summary.
- `POST /positions/refresh`: Auth `Bearer token`; required params `none`; use to force an on-demand holding refresh.
- `GET /watchlist`: Auth `Bearer token`; required params `none`; use for the token owner's watchlist.
- `POST /watchlist/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use to add a stock to the token owner's watchlist.
- `DELETE /watchlist/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use to remove a stock from the token owner's watchlist.
- `GET /search`: Auth `Bearer token`; required params `q`; use for lightweight stock search by code or name.
- `GET /stocks`: Auth `Bearer token`; required params `none`; use for the stock pool list with keyword, board, watchlist, industry, tier, theme, and date filters. Response uses `data.records`.
- `GET /stocks/summary`: Auth `Bearer token`; required params `none`; use for stock pool up/down and limit-up/limit-down summary under the same filters.
- `GET /stocks/filters`: Auth `Bearer token`; required params `none`; use for stock pool filter options such as industries, tiers, and themes.
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
- `GET /stocks/{ts_code}/events/holder-trades`: Auth `Bearer token`; required params path `ts_code`; use for shareholder increase or decrease records keyed by `ann_date`.
- `GET /stocks/{ts_code}/events/block-trades`: Auth `Bearer token`; required params path `ts_code`; use for stock-level block trade records keyed by `trade_date`.
- `GET /stocks/{ts_code}/events/repurchases`: Auth `Bearer token`; required params path `ts_code`; use for repurchase plan and execution progress records keyed by `ann_date`.
- `GET /stocks/{ts_code}/flows/slb-sec-detail`: Auth `Bearer token`; required params path `ts_code`; use for securities lending detail records.
- `GET /concepts/{ts_code}/moneyflow/ths`: Auth `Bearer token`; required params path `ts_code`; use for THS concept moneyflow records.
- `GET /stocks/{ts_code}/ownership/holder-numbers`: Auth `Bearer token`; required params path `ts_code`; use for shareholder-count history keyed by `ann_date` and `end_date`.
- `GET /stocks/{ts_code}/ownership/top10-holders`: Auth `Bearer token`; required params path `ts_code`; use for top10 holder rows keyed by `ann_date`.
- `GET /stocks/{ts_code}/ownership/top10-floatholders`: Auth `Bearer token`; required params path `ts_code`; use for top10 float-holder rows keyed by `ann_date`.
- `GET /stocks/{ts_code}/ownership/overview`: Auth `Bearer token`; required params path `ts_code`; use for an ownership, pledge, repurchase, and block-trade overview in one call.
- `GET /stocks/{ts_code}/capital-overview`: Auth `Bearer token`; required params path `ts_code`; use for a one-call capital and trading overview across moneyflow, margin, HSGT, lending, and toplist context.
- `GET /stocks/{ts_code}/governance-overview`: Auth `Bearer token`; required params path `ts_code`; use for a one-call governance and regulatory overview across surveys, shareholder actions, pledges, unlocks, and related references.
- `GET /stocks/{ts_code}/pledges/detail`: Auth `Bearer token`; required params path `ts_code`; use for pledge detail rows keyed by `ann_date`.
- `GET /stocks/{ts_code}/pledges/stat`: Auth `Bearer token`; required params path `ts_code`; use for pledge summary rows keyed by `end_date`.
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
- `GET /stocks/{ts_code}/top-list-seat-chain`: Auth `Bearer token`; required params path `ts_code`; use for one stock's toplist seat-chain analysis.
- `GET /stocks/{ts_code}/top-list-hot-money`: Auth `Bearer token`; required params path `ts_code`, query `trade_date`, `operate_dept_name`; use to find same-day hot-money candidates linked to a specific operating department.
- `GET /stocks/{ts_code}/top-list-hot-money-buyers`: Auth `Bearer token`; required params path `ts_code`; use for buyer-seat and hot-money clues for a stock.
- `GET /top20/daily`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for a daily score or prediction Top20 snapshot.
- `GET /industries/mappings`: Auth `Bearer token`; required params `none`; use for the industry-to-tier and agent routing map.
- `GET /industries/status`: Auth `Bearer token`; required params `none`; use for industry pipeline freshness and counts.
- `GET /industries/valuation-metrics`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry valuation baselines.
- `GET /industries/factors`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry factor ranking.
- `GET /industries/context`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for merged industry runtime context.
- `GET /industries/events`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for industry event tags with pagination.
- `GET /events/raw`: Auth `Bearer token`; required params `none`; use for原始新闻事件流 evidence, with optional time/source/type filters.
- `GET /index-rebalance-items`: Auth `Bearer token`; scope `market:read`; required params `none`; optional query `ts_code`, `index_code`, `direction` (`in`/`out`), `source_name`, `announce_date`, `effective_date`, `start_effective_date`, `end_effective_date`, `is_active`, `page`, `size`; use for official index rebalance details from `index_rebalance_item`, including index-level 调入/调出 rows. Response uses `data.records`.
- `GET /themes/{theme_code}/overlay`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for theme overlay scores, stance, preferred industries, and preferred stock pool.
- `GET /themes/{theme_code}/stocks`: Auth `Bearer token`; required params `trade_date` or `previous_trade_date=true`; use for the filtered theme stock pool already ranked by overlay priority.
- `GET /theme-stock-pools`: Auth `Bearer token`; required params `none`; use to list available versioned theme pools. Response uses `data.records`.
- `GET /themes/{theme_code}/stock-pool`: Auth `Bearer token`; required params path `theme_code`; optional query `source_version`, `level_code`, `segment_code`, `core_type`, `page`, `size`; use for versioned theme pool members. `level_code` accepts one or multiple values, either comma-separated or repeated. If `source_version` is omitted, backend resolves current/latest. If `level_code` is omitted, backend returns all levels.
- `GET /themes/{theme_code}/stock-pool/ranked`: Auth `Bearer token`; required params path `theme_code`; optional query `source_version`, `level_code`, `trade_date`, `is_active`, `page`, `size`; use for versioned theme pool members sorted by model score/rank. `level_code` accepts one or multiple values; omit it for all levels. `is_active` defaults to active score rows; pass `all` only if the user asks to include inactive scoring rows. Response includes `score_trade_date`, `score_source`, `pool_count`, `ranked_count`, and `records`.
- `GET /themes/{theme_code}/stock-pool/versions`: Auth `Bearer token`; required params path `theme_code`; optional query `limit`; use to list versions of a versioned theme pool.
- `POST /themes/{theme_code}/stock-pool/diagnostics`: Auth `Bearer token`; required params path `theme_code`, JSON `source_version`; optional JSON `level_code` (array/comma string, omit = all non-L5), `end_date` (`YYYYMMDD`); use to start an async pool-effectiveness "四关体检". Returns `{run_id, status:"PENDING"}` immediately; runs ~1-2 min in background, so poll the list/detail endpoints rather than blocking. Load `references/theme-stock-pools.md`.
- `GET /themes/{theme_code}/stock-pool/diagnostics`: Auth `Bearer token`; required params path `theme_code`; optional query `source_version`, `limit`; use to list a version's diagnostic runs (newest first) with `status`/gate fields/`overall_conclusion`; `data.total` = run count. Load `references/theme-stock-pools.md`.
- `GET /themes/{theme_code}/stock-pool/diagnostics/{run_id}`: Auth `Bearer token`; required params path `theme_code`, `run_id`; use to fetch one run's full four-gate report (`report` object with all gate metrics, `overall_conclusion`, `warnings`, `pressure_windows`). Load `references/theme-stock-pools.md`.
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
- `GET /risk-events/market`: Auth `Bearer token`; required params `none`; use for a paged market risk event list with optional date, risk level, and risk domain filters.
- `GET /risk-events/stocks`: Auth `Bearer token`; required params `none`; use for a paged stock risk event list with optional date, stock, risk level, and risk category filters.
- `GET /macro`: Auth `Bearer token`; required params `start_date`, `end_date`; use for a date-ranged macro dataset.
- `POST /screen/stocks`: Auth `Bearer token`; required params JSON `filters`; use for structured stock screening and ranking.
- `GET /market/summary`: Auth `Bearer token`; required params `none`; use for an agent-friendly daily market state payload with subscores, risk flags, and guidance.
- `GET /market/sentiment_pulse`: Auth `Bearer token`; required params `none`; use for an agent-friendly intraday market state payload with subscores, risk flags, and guidance.
- `GET /market/summary/v2`: Auth `Bearer token`; required params `none`; use for the same v2 daily market state payload exposed through the explicit versioned path.
- `GET /market/sentiment_pulse/v2`: Auth `Bearer token`; required params `none`; use for the same v2 intraday market state payload exposed through the explicit versioned path.
- `POST /stocks/{ts_code}/analysis/report`: Auth `Bearer token`; required params path `ts_code`; use to generate an AI valuation report and shareable HTML.
- `GET /valuation`: Auth `Bearer token`; required params `none`; use for the valuation report list with optional `industry`, `tab`, `page`, and `limit`. Response uses `data.records`.
- `GET /valuation/{ts_code}`: Auth `Bearer token`; required params path `ts_code`; use for a single stock's latest valuation report detail.
- `GET /stocks/{ts_code}/balancesheet`: Auth `Bearer token`; required params path `ts_code`; use for raw balance-sheet statement rows.
- `GET /stocks/{ts_code}/cashflow`: Auth `Bearer token`; required params path `ts_code`; use for raw cash-flow statement rows.
- `GET /stocks/{ts_code}/income`: Auth `Bearer token`; required params path `ts_code`; use for raw income-statement rows.
- `GET /stocks/{ts_code}/express`: Auth `Bearer token`; required params path `ts_code`; use for earnings-express rows.
- `GET /health`: Auth `No auth`; required params `none`; use only for a lightweight service liveness check.

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
- Shareholder increase or decrease events -> `GET /stocks/{ts_code}/events/holder-trades`.
- Stock-level block trades and counterparties -> `GET /stocks/{ts_code}/events/block-trades`.
- Repurchase plan or execution progress -> `GET /stocks/{ts_code}/events/repurchases`.
- Shareholder-count trend or ownership breadth -> `GET /stocks/{ts_code}/ownership/holder-numbers`.
- Top10 holder structure -> `GET /stocks/{ts_code}/ownership/top10-holders` or `/stocks/{ts_code}/ownership/top10-floatholders`.
- Pledge detail or pledge summary -> `GET /stocks/{ts_code}/pledges/detail` or `/stocks/{ts_code}/pledges/stat`.
- One-call ownership, pledge, and repurchase overview -> `GET /stocks/{ts_code}/ownership/overview`.
- Daily market state -> `GET /market/summary` or `/market/summary/v2`.
- Intraday market mood -> `GET /market/sentiment_pulse` or `/market/sentiment_pulse/v2`.
- Index rebalance / 调仓 / 调入调出明细 -> `GET /index-rebalance-items`; filter by `announce_date`, `effective_date`, `index_code`, `ts_code`, or `direction`.
- Supply-chain layer or graph structure -> `GET /themes/{theme_code}/supply-chain/graph`.
- Supply-chain segment to impacted companies -> `GET /themes/{theme_code}/supply-chain/exposures`.
- Theme price/funds/valuation pulse -> `GET /themes/{theme_code}/market-pulse`.
- Theme stock-level price/funds/valuation rows -> `GET /themes/{theme_code}/market-stocks`.
- Theme historical price/funds/valuation trend -> `GET /themes/{theme_code}/market-history`.
- Versioned theme pool lookup by version or level -> `GET /themes/{theme_code}/stock-pool`; load `references/theme-stock-pools.md`.
- Versioned theme pool sorted by model score/rank -> `GET /themes/{theme_code}/stock-pool/ranked`; load `references/theme-stock-pools.md`.
- Run / view pool effectiveness "四关体检" diagnostic (是不是真 β、独立性、稳定性、性价比) -> start `POST /themes/{theme_code}/stock-pool/diagnostics`, then poll `GET /themes/{theme_code}/stock-pool/diagnostics` and `GET .../diagnostics/{run_id}`; async (~1-2 min), do not block on the POST; load `references/theme-stock-pools.md`.
- Newly discovered company to A-share candidate mapping -> `GET /themes/{theme_code}/supply-chain/a-share-candidates/search`.
- One event's persisted propagation result -> `GET /events/{event_id}/supply-chain-impact`.

Detailed versioned theme pool semantics live in `references/theme-stock-pools.md`. Keep
`/themes/{theme_code}/stocks` in the event/theme overlay family, and keep
`/themes/{theme_code}/stock-pool*` in the versioned stored pool family.

Mutation safety:

- `POST /positions` and `POST /positions/{position_id}/sell` require explicit user confirmation before calling.
- `POST /stocks/{ts_code}/analysis/report` is allowed only when the user explicitly asks to generate a report.
- Supply-chain maintenance, review, sync, extract, promote, disable, and propagation rerun actions are not routable from this skill; use the Web review/maintenance UI or scheduled pipeline.
