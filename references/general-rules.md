# StockPillar General Rules

## Natural Language To API Mapping

Map user requests to endpoints with the smallest sufficient call set.

## Agent Decision Shortcut

Follow these shortcuts before scanning the detailed mapping:

- "现在 / 当前 / 实时 / 盘中价格" -> `GET /prices/realtime`; supports A-share plus HK/US realtime quote codes.
- "分钟线 / 分时K / 1分钟K线 / 1m bar" -> `GET /stocks/{ts_code}/prices/minute`; supports A-share plus HK/US 1m minute bars.
- "走势 / K线 / 区间涨跌 / 历史价格" -> `GET /stocks/{ts_code}/prices/kline`; supports A-share plus HK/US daily K-line.
- "MA / MACD / RSI / KDJ / BOLL 数值" -> `GET /stocks/{ts_code}/technical/indicators`
- "有没有金叉 / 死叉 / 超买 / 超卖 / 技术异动" -> `GET /stocks/{ts_code}/technical/alerts`
- "全市场扫描 / 哪些股票出现信号" -> `GET /technical/radar`
- "个股资金流 / 主力净流入" -> `GET /stocks/{ts_code}/moneyflow`
- "北向资金 / 沪深港通资金流" -> `GET /moneyflow/hsgt` or `/moneyflow/hsgt/overview`
- "北向持仓 / 港股通持股比例" -> `GET /stocks/{ts_code}/flows/hk-hold`
- "股东增减持 / 谁在减持 / 谁在增持" -> `GET /stocks/{ts_code}/events/holder-trades`
- "大宗交易 / 折价成交 / 接盘方是谁" -> `GET /stocks/{ts_code}/events/block-trades`
- "股票回购 / 回购进度 / 回购金额" -> `GET /stocks/{ts_code}/events/repurchases`
- "股东户数 / 筹码集中度" -> `GET /stocks/{ts_code}/ownership/holder-numbers`
- "前十大股东 / 前十大流通股东" -> `GET /stocks/{ts_code}/ownership/top10-holders` or `/stocks/{ts_code}/ownership/top10-floatholders`
- "股权质押 / 质押比例 / 质押明细" -> `GET /stocks/{ts_code}/pledges/stat` or `/stocks/{ts_code}/pledges/detail`
- "股东结构总览 / 质押回购总览" -> `GET /stocks/{ts_code}/ownership/overview`
- "资金交易总览 / 个股资金画像" -> `GET /stocks/{ts_code}/capital-overview`
- "治理监管总览 / 公司治理风险" -> `GET /stocks/{ts_code}/governance-overview`
- "自选股 / 我的关注" -> `GET /watchlist`
- "股票池 / 股票列表 / 按行业主题筛选" -> `GET /stocks`
- "搜索股票 / 找股票代码" -> `GET /search`
- "估值报告列表 / 估值红榜" -> `GET /valuation`
- "风险事件列表 / 市场风险 / 个股风险" -> `GET /risk-events/market` or `GET /risk-events/stocks`
- "主题池清单 / 有哪些主题池" -> `GET /theme-stock-pools`; then load `references/theme-stock-pools.md`
- "主题池版本 / 版本号" -> `GET /themes/{theme_code}/stock-pool/versions`; then load `references/theme-stock-pools.md`
- "主题池按层级查 / L1 L2 层股票 / 某版本主题池" -> `GET /themes/{theme_code}/stock-pool`; then load `references/theme-stock-pools.md`
- "主题池按模型评分排序 / 主题池评分 TopN" -> `GET /themes/{theme_code}/stock-pool/ranked`; then load `references/theme-stock-pools.md`
- "AI 主题 / AI 供应链 / AI 图谱" -> default `theme_code=AI_EMBODIED`
- "事件如何传导到公司" -> `GET /events/{event_id}/supply-chain-impact`
- "某环节影响哪些公司" -> `GET /themes/{theme_code}/supply-chain/exposures`
- "买入 / 卖出" -> require explicit confirmation before any POST trade endpoint

## Known Theme Codes

- `AI_EMBODIED`: AI与具身智能
  Use this as the default `theme_code` for `/themes/{theme_code}/overlay`, `/themes/{theme_code}/stocks`, `/themes/{theme_code}/daily-brief`, `/themes/{theme_code}/events`, and all `/themes/{theme_code}/supply-chain/*` endpoints unless the user explicitly asks for another theme.
- Versioned theme stock pools are a separate namespace from event/theme overlay analysis. Discover pool
  codes with `GET /theme-stock-pools` and then load `references/theme-stock-pools.md`; do not silently
  map a versioned pool request to `AI_EMBODIED` just because the user says "AI 主题池".

## Naming Semantics

- `flow` means money movement: net inflow, turnover, buy/sell amount, capital direction.
- `holding` means ownership or position: share count, holding ratio, HSGT ownership, portfolio holdings.
- `ownership` means shareholder structure: holder count, top10 holders, top10 float holders, and related overview data.
- `pledge` means share-pledge risk and release state, not money flow.
- Do not use `/stocks/{ts_code}/flows/hk-hold` to answer same-day northbound buying amount. Use it only for holding/ownership questions.
- Do not use `/moneyflow/hsgt` to answer stock-level HSGT ownership. Use it for aggregate money movement.

## Natural Language To Endpoint Mapping

- 单只股票基本信息 -> `GET /stocks/{ts_code}`: Use when the user asks for code, name, industry, area, or listing date. The response also includes `tier` derived from `industry`.
- 多只股票基本信息 -> `GET /stocks/batch?ts_codes=...`: Prefer batch over repeated single calls. Each row also includes `tier`.
- 股票搜索 -> `GET /search?q=...`: Use for quick code/name lookup before calling stock-scoped endpoints when the user gives only a fuzzy company name.
- 股票池列表 -> `GET /stocks`: Use for paged stock-pool browsing with optional `keyword`, `board=all|main|cyb|kcb`, `list_mode=all|watch`, `trade_date`, `industry`, `tier`, and `theme`. Read rows from `data.records`.
- 股票池汇总 -> `GET /stocks/summary`: Use with the same filters as `/stocks` when the user asks for up/down counts or limit-up/limit-down counts.
- 股票池筛选项 -> `GET /stocks/filters`: Use when the user asks what industries, tiers, or themes can be filtered.
- 自选股列表 -> `GET /watchlist`: Use for the token owner's watchlist. Optional `limit`.
- 添加自选股 -> `POST /watchlist/{ts_code}`: Use only when the user explicitly asks to add/follow a stock.
- 删除自选股 -> `DELETE /watchlist/{ts_code}`: Use only when the user explicitly asks to remove/unfollow a stock.
- 分钟线 / 分时K / 1分钟K线 -> `GET /stocks/{ts_code}/prices/minute`: Canonical single-stock same-day 1m minute-bar path; requires `trade_date`, optional `freq=1m`. A-share queries QMT Bridge live, HK/US uses Futu OpenD, and historical minute bars are not skill-visible.
- 历史走势 / 日K / 日线K线 -> `GET /stocks/{ts_code}/prices/kline`: Canonical single-stock daily K-line path; requires `start_date` and `end_date`; supports A-share, HK, and U.S. stocks.
- 实时行情 -> `GET /prices/realtime?ts_codes=...`: Always use `ts_codes`, even for one stock. This endpoint supports A-share codes plus HK/US realtime quote codes such as `00700.HK`, `HK.00700`, `AAPL.US`, or `US.AAPL`.
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
- 股东增减持 / 董监高增减持 -> `GET /stocks/{ts_code}/events/holder-trades`: Use for `holder_name`, `in_de`, `change_vol`, `change_ratio`, `after_share`, `after_ratio`, and `avg_price`.
- 大宗交易 / 折价成交 / 接盘营业部 -> `GET /stocks/{ts_code}/events/block-trades`: Use for `price`, `vol`, `amount`, `buyer`, and `seller`.
- 股票回购 / 回购进度 / 回购金额区间 -> `GET /stocks/{ts_code}/events/repurchases`: Use for `proc`, `vol`, `amount`, `high_limit`, and `low_limit`.
- 股东户数 / 股东人数变化 -> `GET /stocks/{ts_code}/ownership/holder-numbers`: Use for `holder_num` with `ann_date` and `end_date`.
- 前十大股东 / 机构持股结构 -> `GET /stocks/{ts_code}/ownership/top10-holders`: Use for latest or historical holder rows with `hold_ratio`, `hold_change`, and `holder_type`.
- 前十大流通股东 / 流通盘持股结构 -> `GET /stocks/{ts_code}/ownership/top10-floatholders`: Use for float-holder rows and changes.
- 股权质押明细 / 质押解除 / 回购式质押 -> `GET /stocks/{ts_code}/pledges/detail`: Use for pledge timeline, pledgor, release state, and ratios.
- 股权质押统计 / 质押比例 / 质押笔数 -> `GET /stocks/{ts_code}/pledges/stat`: Use for `pledge_count`, `pledge_ratio`, `unrest_pledge`, and `rest_pledge`.
- 股东结构总览 / 质押回购总览 -> `GET /stocks/{ts_code}/ownership/overview`: Use for a one-call overview before deeper endpoint fan-out.
- 资金与交易参考总览 -> `GET /stocks/{ts_code}/capital-overview`: Use before fan-out when the user asks for a broad capital-market picture including moneyflow, margin, HSGT, lending, and toplist context.
- 治理与监管参考总览 -> `GET /stocks/{ts_code}/governance-overview`: Use before fan-out when the user asks for governance, regulatory, shareholder-action, pledge, unlock, or survey context.
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
- 龙虎榜席位链路 -> `GET /stocks/{ts_code}/top-list-seat-chain`: Use when the user asks seat-chain,营业部关系, or repeated-seat clues.
- 龙虎榜游资候选 -> `GET /stocks/{ts_code}/top-list-hot-money`: Requires `trade_date` and `operate_dept_name`; use when drilling into one operating department from a toplist row.
- 龙虎榜买方游资线索 -> `GET /stocks/{ts_code}/top-list-hot-money-buyers`: Use when the user asks which buyer seats or hot-money clues appear for a stock.
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
- 版本化主题池清单 -> `GET /theme-stock-pools`: Use when the user asks which theme pools exist, or before choosing a `theme_code` for versioned pool queries. Load `references/theme-stock-pools.md` for detailed semantics.
- 主题池版本号 -> `GET /themes/{theme_code}/stock-pool/versions`: Use when the user asks what versions a theme pool has. Optional `limit`. Load `references/theme-stock-pools.md`.
- 版本化主题池股票 / 某版本主题池 / 按层级查主题池 -> `GET /themes/{theme_code}/stock-pool`: Use for stored theme pool members. Optional `source_version`; omit it when the user does not pass a version or asks for latest/current. Optional `level_code` supports comma-separated or repeated values; omit it for all levels. Optional `segment_code`, `core_type`, `page`, and `size`. Load `references/theme-stock-pools.md`.
- 主题池按模型评分排序 / 主题池评分 TopN -> `GET /themes/{theme_code}/stock-pool/ranked`: Use for stored theme pool members sorted by the model score/rank. Optional `source_version`; omit it when not specified. Optional `level_code` supports multi-select; omit it for all levels. Optional `trade_date`; omit it to let backend resolve the default scoring date. Optional `is_active=true|false|all`; default active-only. Load `references/theme-stock-pools.md`.
- 主题日评 / 今天 AI 主题怎么总结 -> `GET /themes/{theme_code}/daily-brief`: Use for cached daily theme analysis with `theme_status`, `primary_drivers`, `bullish_points`, `risk_points`, `representative_stocks`, and `summary`. Prefer this before asking the agent to free-form summarize the same day again.
- 主题资金流 / AI 主题今天资金和涨跌怎么样 -> `GET /themes/{theme_code}/market-pulse`: Use for theme-level aggregation by `chain_code`, `layer_index`, `exposure_type`, `relation_strength`, or `segment`.
- 主题相关股票行情资金明细 -> `GET /themes/{theme_code}/market-stocks`: Use when the user asks which theme-related stocks are moving, with supply-chain reason, price change, turnover, main moneyflow, and valuation.
- 主题历史表现 / 一段时间 AI 主题涨跌资金估值变化 -> `GET /themes/{theme_code}/market-history`: Use for historical trend aggregation from `kline_daily`, `moneyflow`, and `valuation_data`.
- 主题事件影响 / 主题为什么加分 -> `GET /themes/{theme_code}/events`: Use for theme-level evidence with `importance_score`, `sentiment`, `impact_direction`, and `mapping_confidence`.
- 主题供应链图谱 / AI 产业链六层结构 / 图谱有哪些公司 -> `GET /themes/{theme_code}/supply-chain/graph`: Use for layered supply-chain nodes, edges, and company exposure edges. L0 is `power_infra` / 电力与能源底座.
- 供应链候选关系 / 哪些关系待审核 -> `GET /themes/{theme_code}/supply-chain/candidates`: Use for AI-extracted candidate relations and review status.
- 供应链公司池 / 某一环节影响哪些公司 -> `GET /themes/{theme_code}/supply-chain/exposures`: Use for the reviewed company exposure pool.
- 今日/某日 AI 供应链影响了哪些公司 -> `GET /themes/{theme_code}/supply-chain/impacts`: Use for date-level persisted propagation summaries and coverage status. Check `coverage` before saying there are no impacts.
- 某只股票在供应链哪里 -> `GET /stocks/{ts_code}/supply-chain`: Use for a stock's mapped supply-chain position.
- 某条新闻如何沿供应链传导 -> `GET /events/{event_id}/supply-chain-impact`: Use for persisted event-to-company propagation results.
- 重新跑某事件供应链传导 -> do not route from this skill. Explain that event propagation reruns are handled by the web maintenance UI or scheduled pipeline.
- 个股事件影响 / 这条新闻是否影响某只股票 -> `GET /stocks/{ts_code}/events`: Use for stock-level mapped event evidence.
- 事件打分是否有效 / 事件后验表现 / 回测校准 -> `GET /events/outcomes`: Use for post-event market feedback such as T+1/T+5 returns and outcome labels.
- 市场风险事件列表 -> `GET /risk-events/market`: Use for paged market risk events with `start_date`, `end_date`, `risk_level`, and `risk_domain` filters.
- 个股风险事件列表 -> `GET /risk-events/stocks`: Use for paged stock risk events with `start_date`, `end_date`, `ts_code`, `stock_name`, `risk_level`, and `risk_category` filters.
- 宏观数据 -> `GET /macro`: Prefer a date range if the user mentions time.
- 条件选股 -> `POST /screen/stocks`: Use structured JSON `filters`.
- 市场状态评分 -> `GET /market/summary`: Use when the user wants an agent-friendly daily market score with subscores, flags, and guidance.
- 盘中市场状态评分 -> `GET /market/sentiment_pulse`: Use when the user wants an agent-friendly intraday market score with subscores, flags, and guidance.
- AI 价值研报 -> `POST /stocks/{ts_code}/analysis/report`: Canonical single-stock report path; use only when the user explicitly wants a report.
- 估值报告列表 -> `GET /valuation`: Use for valuation report list, valuation red-list style browsing, and filtering by `industry` or `tab`. Read rows from `data.records`.
- 估值报告详情 -> `GET /valuation/{ts_code}`: Use for one stock's latest saved valuation report detail.
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
- HK/US stocks support `GET /prices/realtime`, `GET /stocks/{ts_code}/prices/minute` for same-day 1m bars, and `GET /stocks/{ts_code}/prices/kline` for historical daily K-line. U.S. `.US` stocks also support SEC-derived `/financial`, `/income`, `/balancesheet`, and `/cashflow`. Use suffix form (`00700.HK`, `AAPL.US`) by default, or accept Futu prefix form (`HK.00700`, `US.AAPL`) when the user provides it.
- If the user gives only a six-digit code and the exchange is obvious from prior context, infer cautiously.
- If the user gives a Hong Kong numeric code without a market suffix, do not guess silently unless prior context makes `.HK` clear; Hong Kong codes are zero-padded to five digits by the backend for realtime quotes.
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
- `/stocks/{ts_code}/events/holder-trades`, `/stocks/{ts_code}/events/repurchases`, `/stocks/{ts_code}/ownership/holder-numbers`, `/stocks/{ts_code}/ownership/top10-holders`, `/stocks/{ts_code}/ownership/top10-floatholders`, and `/stocks/{ts_code}/pledges/detail` use `ann_date` for an exact disclosure date; `trade_date` is accepted as an alias when the user just says "当天公告".
- `/stocks/{ts_code}/pledges/stat` uses `trade_date` as the exact snapshot-date alias for `end_date`; for ranges, use `start_date` and `end_date`.
- `/stocks/{ts_code}/prices/limits`, `/stocks/{ts_code}/events/suspend`, `/stocks/{ts_code}/flows/hk-hold`, `/stocks/{ts_code}/technical/cyq-perf`, `/stocks/{ts_code}/technical/cyq-chips`, `/stocks/{ts_code}/events/limit-list`, `/stocks/{ts_code}/flows/slb-sec-detail`, and `/concepts/{ts_code}/moneyflow/ths` accept `trade_date` for an exact day or `start_date`/`end_date` for a range.
- `/stocks/{ts_code}/prices/minute` requires exact `trade_date`; do not use `start_date`/`end_date` for this endpoint.
- If user asks "recent", "最近", or "近期" without a range:
  - technical indicators: default to last 60 calendar days
  - minute bars: ask for or infer a specific `trade_date`; prefer today only when the user asks for today's intraday/minute data
  - K-line: default to last 30 calendar days
  - shareholder trade, block trade, repurchase, pledge detail, and ownership overview event lists: default to last 180 calendar days
  - holder-number, top10 holders, top10 float holders, and pledge stat snapshots: default to latest available rows when no explicit range is given
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
- `source_version`: use only for versioned theme pool endpoints. Omit it for latest/current behavior.
- `level_code`: use only for versioned theme pool endpoints. It can be a single layer (`L1`) or multi-select (`L1,L2`, repeated params). Omit it for all levels.
- `segment_code` and `core_type`: use only for `/themes/{theme_code}/stock-pool`.
- `is_active`: use only for `/themes/{theme_code}/stock-pool/ranked`; pass `all` only when the user asks to include inactive score rows.
- For all four options above, load `references/theme-stock-pools.md`; they do not belong to
  event/theme overlay endpoints in `references/industries-events.md`.
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
