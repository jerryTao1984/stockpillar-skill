# StockPillar General Rules

## Natural Language To API Mapping

Map user requests to endpoints with the smallest sufficient call set.

## Agent Decision Shortcut

Follow these shortcuts before scanning the detailed mapping:

- "现在 / 当前 / 实时 / 盘中价格" -> `GET /prices/realtime`
- "走势 / K线 / 区间涨跌 / 历史价格" -> `GET /stocks/{ts_code}/prices/kline`
- "MA / MACD / RSI / KDJ / BOLL 数值" -> `GET /stocks/{ts_code}/technical/indicators`
- "有没有金叉 / 死叉 / 超买 / 超卖 / 技术异动" -> `GET /stocks/{ts_code}/technical/alerts`
- "全市场扫描 / 哪些股票出现信号" -> `GET /technical/radar`
- "个股资金流 / 主力净流入" -> `GET /stocks/{ts_code}/moneyflow`
- "北向资金 / 沪深港通资金流" -> `GET /moneyflow/hsgt` or `/moneyflow/hsgt/overview`
- "北向持仓 / 港股通持股比例" -> `GET /stocks/{ts_code}/flows/hk-hold`
- "AI 主题 / AI 供应链 / AI 图谱" -> default `theme_code=AI_EMBODIED`
- "事件如何传导到公司" -> `GET /events/{event_id}/supply-chain-impact`
- "某环节影响哪些公司" -> `GET /themes/{theme_code}/supply-chain/exposures`
- "主题股票池 / 核心层 / 观察层 / 概念层 / L1 / L2 / L3 / L4 / L5 / 核心跟踪股 / 当前版本池 / 版本化股票池" -> `GET /themes/{theme_code}/stock-pool`
- "主题池历史版本 / 池子是哪一版 / 上一版股票池" -> `GET /themes/{theme_code}/stock-pool/versions`
- "今天主题里挑哪些 / 今日 overlay 偏好" -> `GET /themes/{theme_code}/stocks` (overlay daily, **not** stock-pool)
- "自选股 / 关注列表" -> `GET /watchlist` (read), `POST /watchlist/{ts_code}` (add), `DELETE /watchlist/{ts_code}` (remove)
- "市场风险事件 / 全市场风险预警 / regime shift" -> `GET /risk-events/market` or `GET /market/regime_events`
- "个股风险事件 / 硬风险 / 退市风险 / 监管风险" -> `GET /risk-events/stocks` or `GET /stocks/{ts_code}/events?risk_level=hard`
- "估值列表 / 估值榜 / 当前估值情况" -> `GET /valuation`
- "某只股票估值 / DCF / 估值快照" -> `GET /valuation/{ts_code}`
- "持股变动 / 股东减持增持" -> `GET /stocks/{ts_code}/events/holder-trades`
- "大宗交易" -> `GET /stocks/{ts_code}/events/block-trades`
- "回购 / 股份回购" -> `GET /stocks/{ts_code}/events/repurchases`
- "股东人数 / 户数变化" -> `GET /stocks/{ts_code}/ownership/holder-numbers`
- "十大股东 / 前十大股东" -> `GET /stocks/{ts_code}/ownership/top10-holders`
- "十大流通股东" -> `GET /stocks/{ts_code}/ownership/top10-floatholders`
- "质押明细 / 大股东质押" -> `GET /stocks/{ts_code}/pledges/detail`
- "质押统计 / 质押比例" -> `GET /stocks/{ts_code}/pledges/stat`
- "股东结构总览" -> `GET /stocks/{ts_code}/ownership/overview`
- "股本/资本结构总览" -> `GET /stocks/{ts_code}/capital-overview`
- "公司治理总览" -> `GET /stocks/{ts_code}/governance-overview`
- "龙虎榜席位链路 / 游资席位关联" -> `GET /stocks/{ts_code}/top-list-seat-chain`
- "游资 / 热钱 / 知名游资买入" -> `GET /stocks/{ts_code}/top-list-hot-money` (席位) 或 `/top-list-hot-money-buyers` (买方)
- "主题列表 / 有哪些主题" -> `GET /themes`
- "主题相关视频 / 新闻视频" -> `GET /themes/{theme_code}/news-videos`
- "主题信源质量 / 来源审计" -> `GET /themes/{theme_code}/supply-chain/quality-audit`
- "国产替代 / 国产化进度" -> `GET /themes/{theme_code}/supply-chain/domestic-substitution`
- "信源矩阵 / 信源覆盖" -> `GET /themes/{theme_code}/supply-chain/source-matrix`
- "研报纪要 / 调研纪要 / 路演纪要" -> `GET /research-meetings` (列表) / `GET /research-meetings/{id}` (详情) / `GET /research-meetings/candidates` (候选标的)
- "搜股票 / 模糊搜索" -> `GET /search`
- "全市场股票列表 / 股票池筛选" -> `GET /stocks` (+ `GET /stocks/summary` / `GET /stocks/filters` 取过滤项)
- "买入 / 卖出" -> require explicit confirmation before any POST trade endpoint

## Known Theme Codes

- `AI_EMBODIED`: AI与具身智能
  Use this as the default `theme_code` for `/themes/{theme_code}/overlay`, `/themes/{theme_code}/stocks`, `/themes/{theme_code}/daily-brief`, `/themes/{theme_code}/events`, and all `/themes/{theme_code}/supply-chain/*` endpoints unless the user explicitly asks for another theme.

## Naming Semantics

- `flow` means money movement: net inflow, turnover, buy/sell amount, capital direction.
- `holding` means ownership or position: share count, holding ratio, HSGT ownership, portfolio holdings.
- Do not use `/stocks/{ts_code}/flows/hk-hold` to answer same-day northbound buying amount. Use it only for holding/ownership questions.
- Do not use `/moneyflow/hsgt` to answer stock-level HSGT ownership. Use it for aggregate money movement.

Common position-oriented `query_type` mapping:

- `positions` -> `GET /positions`
- `position_trades` -> `GET /positions/trades`
- `position_summary` -> `GET /positions/summary`
- `position_refresh` -> `POST /positions/refresh`

Common industry-oriented `query_type` mapping:

- `industry_status` -> `GET /industries/status`
- `industry_mappings` -> `GET /industries/mappings`
- `industry_valuation_metrics` -> `GET /industries/valuation-metrics`
- `industry_factors` -> `GET /industries/factors`
- `industry_context` -> `GET /industries/context`
- `industry_events` -> `GET /industries/events`

Common event-evidence `query_type` mapping:

- `raw_events` -> `GET /events/raw`
- `theme_overlay` -> `GET /themes/{theme_code}/overlay`
- `theme_stocks` -> `GET /themes/{theme_code}/stocks`
- `theme_daily_brief` -> `GET /themes/{theme_code}/daily-brief`
- `theme_market_pulse` -> `GET /themes/{theme_code}/market-pulse`
- `theme_market_stocks` -> `GET /themes/{theme_code}/market-stocks`
- `theme_market_history` -> `GET /themes/{theme_code}/market-history`
- `theme_events` -> `GET /themes/{theme_code}/events`
- `stock_events` -> `GET /stocks/{ts_code}/events`
- `event_outcomes` -> `GET /events/outcomes`

Common margin-oriented `query_type` mapping:

- `margin_summary` -> `GET /margin/summary`
- `margin_detail` -> `GET /margin/detail`

- 单只股票基本信息 -> `GET /stocks/{ts_code}`: Use when the user asks for code, name, industry, area, or listing date. The response also includes `tier` derived from `industry`.
- 多只股票基本信息 -> `GET /stocks/batch?ts_codes=...`: Prefer batch over repeated single calls. Each row also includes `tier`.
- 历史走势 / K线 -> `GET /stocks/{ts_code}/prices/kline`: Canonical single-stock K-line path; requires `start_date` and `end_date`.
- 实时行情 -> `GET /prices/realtime?ts_codes=...`: Always use `ts_codes`, even for one stock.
- 技术指标数值 -> `GET /stocks/{ts_code}/technical/indicators`: Canonical single-stock indicator path; use grouped indicator families such as MA, EMA, MACD, RSI, KDJ, BOLL, and VOL_MA.
- 技术异动信号 -> `GET /stocks/{ts_code}/technical/alerts`: Canonical single-stock alert path; use for gold cross, oversold, breakout, and similar signals.
- 涨跌停价格 / 涨停价 / 跌停价 -> `GET /stocks/{ts_code}/prices/limits`: Use for trading constraint checks and limit-up or limit-down price facts.
- 停牌 / 复牌 / 不可交易 -> `GET /stocks/{ts_code}/events/suspend`: Use for suspension or resumption event checks.
- 港股通持股 / 北向持仓 / 外资持股 -> `GET /stocks/{ts_code}/flows/hk-hold`: Use for stock-level HSGT holding changes, not turnover flow.
- 限售解禁 / 解禁压力 -> `GET /stocks/{ts_code}/events/share-float`: Use for restricted-share unlock events and risk context.
- 筹码分布参考 / 获利盘 / 成本分位 -> `GET /stocks/{ts_code}/technical/cyq-perf`: Use for `cyq_perf` fields such as `winner_rate`, `cost_5pct`, `cost_50pct`, and `weight_avg`.
- 筹码价格档 / 筹码明细 -> `GET /stocks/{ts_code}/technical/cyq-chips`: Use for `cyq_chips` price-bucket records with `price` and `percent`.
- 涨停列表 / 跌停列表 / 连板 -> `GET /stocks/{ts_code}/events/limit-list`: Use for board-list facts such as `limit_type`, `open_times`, `limit_times`, and seal strength.
- 机构调研 / 投资者关系 / 调研内容 -> `GET /stocks/{ts_code}/events/surveys`: Use for `stk_surv` survey date, visitor, reception, and content records.
- 转融券 / 融券出借费率 / 转融券数量 -> `GET /stocks/{ts_code}/flows/slb-sec-detail`: Use for securities lending `tenor`, `lending_rate`, and `vol`.
- 同花顺概念资金流 / 概念板块资金 -> `GET /concepts/{ts_code}/moneyflow/ths`: Use for THS concept-level moneyflow, not individual stock moneyflow.
- 全市场技术扫描 -> `GET /technical/radar`: Use for market-wide scanning.
- 个股资金流 -> `GET /stocks/{ts_code}/moneyflow`: Canonical single-stock moneyflow path; requires a date range.
- 沪深港通资金 -> `GET /moneyflow/hsgt`: Requires `start_date` and `end_date`.
- 沪深港通总览 -> `GET /moneyflow/hsgt/overview`: Best for a one-day northbound summary, 沪/深拆分, and Top10 active names.
- 沪深港通Top10 -> `GET /moneyflow/hsgt/top10`: Query active stocks by `trade_date` or date range.
- 两融汇总 -> `GET /margin/summary`: Supports `trade_date` or date range. Optional `exchange_id=SSE|SZSE|BSE`.
- 两融明细 -> `GET /margin/detail`: Supports `trade_date` or date range. Optional `ts_code`.
- 单只股票两融明细 -> `GET /stocks/{ts_code}/margin`: Canonical single-stock margin-detail path; optional date or range.
- 综合财务指标 -> `GET /stocks/{ts_code}/financial`: Canonical financial summary path; use `period=latest` unless the user asks for history.
- 资产负债表 -> `GET /stocks/{ts_code}/balancesheet`: Canonical balance-sheet path.
- 现金流量表 -> `GET /stocks/{ts_code}/cashflow`: Canonical cash-flow path.
- 利润表 -> `GET /stocks/{ts_code}/income`: Canonical income-statement path.
- 业绩快报 -> `GET /stocks/{ts_code}/express`: Canonical earnings-express path.
- 龙虎榜总览 -> `GET /toplist`: Best for a latest market-wide toplist or one-day toplist snapshot.
- 龙虎榜 -> `GET /stocks/{ts_code}/toplist`: Canonical single-stock toplist path; optional `trade_date`.
- 每日 Top20 榜单 -> `GET /top20/daily?trade_date=YYYYMMDD&type=score_top20|prediction_top20`: `type` is optional. Omit it to fetch both lists; pass it to query one list only. If the user wants the previous trading day, prefer `previous_trade_date=true` instead of making the agent calculate the date.
- 行业运行状态 -> `GET /industries/status`: Returns the latest dates and counts for mappings, valuation metrics, factors, context, and events.
- 行业映射 -> `GET /industries/mappings`: Returns `industry_name`, `config_tier`, and `agent_type` for routing and grouping.
- 行业估值基线 -> `GET /industries/valuation-metrics`: Requires `trade_date` or `previous_trade_date=true`; supports optional `industry_name`.
- 行业因子榜 -> `GET /industries/factors`: Requires `trade_date` or `previous_trade_date=true`; supports optional `industry_name` and `agent_type`.
- 行业上下文 -> `GET /industries/context`: Requires `trade_date` or `previous_trade_date=true`; includes tier, agent routing, valuation, and trading context.
- 行业事件标签 -> `GET /industries/events`: Requires `trade_date` or `previous_trade_date=true`; supports optional `industry_name`, `agent_type`, and pagination.
- 原始新闻事件流 / 财联社快讯 / 东方财富快讯 / 公告事件 -> `GET /events/raw`: Use when the user needs raw event evidence before scoring or mapping.
- 主题当天总状态 / 今天 AI 主题强弱如何 -> `GET /themes/{theme_code}/overlay`: Use for the current overlay score, event-adjusted score, stance, preferred industries, and preferred stock pool.
- 主题股票池 / AI 主题核心股有哪些 -> `GET /themes/{theme_code}/stocks`: Use for theme-scoped stocks that have already been filtered and ranked by overlay priority.
- 主题日评 / 今天 AI 主题怎么总结 -> `GET /themes/{theme_code}/daily-brief`: Use for cached daily theme analysis with `theme_status`, `primary_drivers`, `bullish_points`, `risk_points`, `representative_stocks`, and `summary`. Prefer this before asking the agent to free-form summarize the same day again.
- 主题资金流 / AI 主题今天资金和涨跌怎么样 -> `GET /themes/{theme_code}/market-pulse`: Use for theme-level aggregation by `chain_code`, `layer_index`, `exposure_type`, `relation_strength`, or `segment`.
- 主题相关股票行情资金明细 -> `GET /themes/{theme_code}/market-stocks`: Use when the user asks which theme-related stocks are moving, with supply-chain reason, price change, turnover, main moneyflow, and valuation.
- 主题历史表现 / 一段时间 AI 主题涨跌资金估值变化 -> `GET /themes/{theme_code}/market-history`: Use for historical trend aggregation from `kline_daily`, `moneyflow`, and `valuation_data`.
- 主题事件影响 / 主题为什么加分 -> `GET /themes/{theme_code}/events`: Use for theme-level evidence with `importance_score`, `sentiment`, `impact_direction`, and `mapping_confidence`.
- 主题供应链图谱 / AI 产业链五层结构 / 图谱有哪些公司 -> `GET /themes/{theme_code}/supply-chain/graph`: Use for layered supply-chain nodes, edges, and company exposure edges.
- 供应链候选关系 / 哪些关系待审核 -> `GET /themes/{theme_code}/supply-chain/candidates`: Use for AI-extracted candidate relations and review status.
- 供应链公司池 / 某一环节影响哪些公司 -> `GET /themes/{theme_code}/supply-chain/exposures`: Use for the reviewed company exposure pool.
- 今日/某日 AI 供应链影响了哪些公司 -> `GET /themes/{theme_code}/supply-chain/impacts`: Use for date-level persisted propagation summaries and coverage status. Check `coverage` before saying there are no impacts.
- 某只股票在供应链哪里 -> `GET /stocks/{ts_code}/supply-chain`: Use for a stock's mapped supply-chain position.
- 某条新闻如何沿供应链传导 -> `GET /events/{event_id}/supply-chain-impact`: Use for persisted event-to-company propagation results.
- 重新跑某事件供应链传导 -> do not route from this skill. Explain that event propagation reruns are handled by the web maintenance UI or scheduled pipeline.
- 个股事件影响 / 这条新闻是否影响某只股票 -> `GET /stocks/{ts_code}/events`: Use for stock-level mapped event evidence.
- 事件打分是否有效 / 事件后验表现 / 回测校准 -> `GET /events/outcomes`: Use for post-event market feedback such as T+1/T+5 returns and outcome labels.
- 宏观数据 -> `GET /macro`: Prefer a date range if the user mentions time.
- 条件选股 -> `POST /screen/stocks`: Use structured JSON `filters`.
- 市场状态评分 -> `GET /market/summary`: Use when the user wants an agent-friendly daily market score with subscores, flags, and guidance.
- 盘中市场状态评分 -> `GET /market/sentiment_pulse`: Use when the user wants an agent-friendly intraday market score with subscores, flags, and guidance.
- AI 价值研报 -> `POST /stocks/{ts_code}/analysis/report`: Canonical single-stock report path; use only when the user explicitly wants a report.
- 健康检查 -> `GET /health`: No auth required; use only for service availability checks.
- 持仓列表 -> `GET /positions`: Optional `status=holding`; PnL is computed from realtime quotes at read time and includes per-position trading-cost fields.
- 买入持仓 -> `POST /positions`: JSON body requires `ts_code`, `qty`, `cost_price`.
- 卖出持仓 -> `POST /positions/{position_id}/sell`: Use for real sell actions. The JSON body can pass `qty` for a partial sell.
- 交易流水 -> `GET /positions/trades`: Query historical buy or sell executions for analysis; supports pagination and aggregate summary.
- 持仓汇总 -> `GET /positions/summary`: Summary is computed from realtime quotes at read time and includes portfolio-level cost fields.
- 刷新持仓盈亏 -> `POST /positions/refresh`: Forces an on-demand recompute from realtime quotes and returns the result; no position-row price writeback.

## Parameter Normalization

Normalize before constructing the request.

### Stock Codes

- A-share stocks must include exchange suffix: `600519.SH`, `000001.SZ`, `830946.BJ`.
- If the user gives only a six-digit code and the exchange is obvious from prior context, infer cautiously.
- If the code is ambiguous or you cannot resolve it confidently, ask.
- `GET /stocks/{ts_code}` and `GET /stocks/batch` return a normalized `tier` field derived from the stock's `industry`.

### Dates

All API dates use `YYYYMMDD`.

Defaults:

- `trade_date`: use only when the user asks for a specific day or "today".
- `daily_top20` requires either `trade_date` or `previous_trade_date=true`.
- `industry_valuation_metrics`, `industry_factors`, `industry_context`, and `industry_events` also require either `trade_date` or `previous_trade_date=true`.
- `theme_overlay`, `theme_stocks`, and `theme_daily_brief` also require either `trade_date` or `previous_trade_date=true`.
- `raw_events`, `theme_events`, and `stock_events` can use either `trade_date` / `previous_trade_date=true` or explicit `start_time` / `end_time`. Do not pass `trade_date` together with `start_time` or `end_time`.
- `event_outcomes` can use either `trade_date` / `previous_trade_date=true` or explicit `start_trade_date` / `end_trade_date`. Do not mix exact `trade_date` with an explicit outcome date range.
- If the user says "上一个交易日", prefer `previous_trade_date=true` instead of making the agent calculate the calendar date.
- `start_date` and `end_date`: prefer explicit ranges.
- `/stocks/{ts_code}/events/share-float` uses `float_date` for an exact unlock date; otherwise use `start_date` and `end_date` as the unlock-date range.
- `/stocks/{ts_code}/events/surveys` uses `surv_date` for an exact survey date; `trade_date` is accepted as an alias when the user says "当天".
- `/stocks/{ts_code}/prices/limits`, `/stocks/{ts_code}/events/suspend`, `/stocks/{ts_code}/flows/hk-hold`, `/stocks/{ts_code}/technical/cyq-perf`, `/stocks/{ts_code}/technical/cyq-chips`, `/stocks/{ts_code}/events/limit-list`, `/stocks/{ts_code}/flows/slb-sec-detail`, and `/concepts/{ts_code}/moneyflow/ths` accept `trade_date` for an exact day or `start_date`/`end_date` for a range.
- If user asks "recent", "最近", or "近期" without a range:
  - technical indicators: default to last 60 calendar days
  - K-line: default to last 30 calendar days
  - limit price, suspension, HSGT holding, share-unlock, limit-list, survey, securities-lending, and THS concept-flow events: default to last 30 calendar days
  - chip-distribution endpoints: default to last 30 calendar days unless the user asks for a specific day
  - money flow: default to last 10 calendar days
  - financial statements: default to `period=latest`

### Single vs Batch

- `/prices/realtime` expects `ts_codes`, not `ts_code`.
- `/stocks/{ts_code}` is single-stock only.
- For single-stock APIs, prefer the canonical `/stocks/{ts_code}/...` form whenever that form exists.
- Do not invent alternate REST paths beyond the exact endpoint patterns defined in this skill.
- Prefer batch endpoints when the user asks about multiple securities.

### Common Optional Flags

- `refresh=true|1|yes`: only use when the user explicitly wants a refresh or recompute on endpoints that implement it, such as `/top20/daily`.
- Do not add `refresh` by default for read requests.
- Do not use `refresh` with `/positions` or `/positions/summary`; use `POST /positions/refresh` when the user wants a portfolio recompute.
- `status=holding`: use only for `/positions`. Legacy `持有` still works but should not be preferred by the agent.
- `order_type=买入|卖出`: use only for `/positions/trades`.
- `industry_name`: use only for `/industries/valuation-metrics`, `/industries/factors`, `/industries/context`, `/industries/events`.
- `agent_type`: use only for `/industries/factors`, `/industries/context`, `/industries/events`.
- `ingest_source`: use only for `/events/raw`; examples are `cls_roll_list`, `eastmoney_kuaixun`, `akshare`.
- `content_source_type`: use only for `/events/raw`; examples are `announcement`, `policy_news`, `finance_news`.
- `event_type` and `sentiment`: use only for event tag endpoints such as `/themes/{theme_code}/events` and `/stocks/{ts_code}/events`.
- `risk_level` and `risk_category`: use only for `/stocks/{ts_code}/events`. Prefer `risk_level=hard` when the user asks for hard-risk alerts, forced-sell risk evidence, or urgent stock-specific risk news.
- `stock_limit`: use only for `/themes/{theme_code}/overlay` and `/themes/{theme_code}/stocks`.
- `group_by`: use on `/themes/{theme_code}/market-pulse` or `/themes/{theme_code}/market-history`; supported values are `chain_code`, `layer_index`, `exposure_type`, `relation_strength`, and `segment`.
- `sort_by`: use on `/themes/{theme_code}/market-stocks`; supported values include `pct_chg`, `amount`, `main_net_inflow`, `exposure_score`, `turnover_rate`, `total_mv`, `pe_ttm`, and `pb`.
- `start_date` and `end_date`: required for `/themes/{theme_code}/market-history`; format `YYYYMMDD` or `YYYY-MM-DD`; maximum range is 370 calendar days.
- Do not use `force_refresh=true` from this skill. Theme daily-brief regeneration is a web maintenance or scheduled pipeline action.
- `chain_code`: use only for supply-chain graph/exposure reads when selecting a specific supply-chain graph under a theme.
- `layer_index`: use only for `/themes/{theme_code}/supply-chain/graph` to query one layer of the graph.
- `include_pending=true`: use only for `/themes/{theme_code}/supply-chain/graph` when the user explicitly wants unapproved graph edges included.
- `include_inactive=true`: use only for `/themes/{theme_code}/supply-chain/graph` when auditing disabled or inactive graph data.
- `review_status`: use only for supply-chain candidate and exposure endpoints; common values are `pending`, `auto_approved`, `approved`, and `rejected`.
- `source_event_id` / `event_id`: use on supply-chain candidate endpoints to filter candidates from a specific source event.
- `segment_node_id` and `company_node_id`: use only for `/themes/{theme_code}/supply-chain/exposures`.
- `target_type`, `target_id`, and `outcome_label`: use only for `/events/outcomes`.
- `exchange_id`: use only for `/margin/summary`; supported values are `SSE`, `SZSE`, `BSE`.
- `period=latest` is the preferred default for `/stocks/{ts_code}/financial`, `/stocks/{ts_code}/balancesheet`, `/stocks/{ts_code}/cashflow`, `/stocks/{ts_code}/income`, `/stocks/{ts_code}/express`.
- If `period` is not `latest`, it must be a positive integer string.
- If the API returns `400`, first check whether query params or request shape are invalid before retrying.

## Core Execution Pattern

Use this pattern unless the task clearly requires something else:

1. Identify intent.
2. Normalize stock code and dates.
3. Pick one endpoint.
4. Only combine endpoints when the user asked for mixed dimensions such as `价格 + 技术指标` or `技术信号 + 基本面`.
5. Summarize the data in plain Chinese, with dates and metric names.

## Response Contract

Skill responses always use:

- `code`
- `message`
- `data`

When the backend service result contains pagination metadata and `data` is an object, the skill response merges these fields into `data`:

- `page`
- `size`
- `total`

Do not assume `page`, `size`, or `total` appear at the top level of the JSON body.
