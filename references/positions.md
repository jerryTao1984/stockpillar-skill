# StockPillar Positions Reference

## Trade Safety Rules

These rules override all other position endpoint guidance:

- Never call `POST /positions` or `POST /positions/{position_id}/sell` from vague wording.
- Explicit confirmation is required in the current conversation before any buy or sell POST.
- Vague phrases such as "买点", "卖点", "帮我操作", "要不要上", or "看着办" are not confirmation.
- If the user gives intent but not confirmation, summarize the proposed order and ask for confirmation.
- Confirmation must include or clearly confirm the stock or position, side, quantity, and price or cost basis.
- Read-only endpoints do not require confirmation: `GET /positions`, `GET /positions/summary`, `GET /positions/trades`.

Safe handling examples:

- User: "买点茅台吧" -> do not POST. Ask for quantity, cost price, and confirmation.
- User: "按 1500 买入 600519.SH 100 股，确认执行" -> POST can be used if all required fields are present.
- User: "卖出 position_id=12 100 股，确认" -> sell POST can be used.

## `/positions` Guide

Use the position endpoints when the user asks for:

- 当前持仓列表
- 当前组合盈亏和汇总
- 买入或卖出一条持仓
- 查询逐笔交易流水
- 按实时行情重算持仓盈亏

### When To Use Which Endpoint

- `GET /positions`: use for current holdings or filtered holdings
- `GET /positions/summary`: use for portfolio-level summary only
- `POST /positions`: use to execute a buy and update current holdings
- `POST /positions/{position_id}/sell`: use to execute a sell against an existing holding
- `GET /positions/trades`: use to review historical buy/sell executions
- `POST /positions/refresh`: use only when the user explicitly wants an on-demand recompute

### Required And Optional Fields

- `POST /positions` requires `ts_code`, `qty`, `cost_price`
- `POST /positions/{position_id}/sell` accepts optional `qty`; omit it to sell the full remaining position
- `ts_code` must include exchange suffix such as `600519.SH`
- `name` is optional; backend may fill it from stock master data
- `position_date` uses `YYYYMMDD`
- `commission_rate`, `slippage_rate`, and `stamp_tax_rate` are optional
- Default cost assumptions follow A-share defaults: `commission_rate=0.0003`, `slippage_rate=0.001`, `stamp_tax_rate=0.0005`
- These are system-level default assumptions. Actual rates may differ from the user's brokerage agreement.
- `GET /positions` optionally accepts `status=holding`; legacy `持有` still works but should not be preferred by the agent
- `GET /positions/trades` supports `ts_code`, `order_type=买入|卖出`, `start_date`, `end_date`, `page`, `size`

### `/positions/trades` Query Guide

Use `GET /positions/trades` when the user asks for:

- 某只股票的买卖流水
- 最近一段时间的成交记录
- 买入记录或卖出记录复盘
- 手续费、滑点、印花税等逐笔成交分析

Recommended filters:

- `ts_code`: narrow to one stock when the user is reviewing a specific name
- `order_type=买入|卖出`: use when the user only wants buy-side or sell-side executions
- `start_date` and `end_date`: use explicit date ranges whenever the user gives one
- `page`: default to `1` unless the user explicitly asks for later pages
- `size`: use to control page size; backend caps it at `500`

Important response fields:

- `order_type`: `买入` or `卖出`
- `qty`: executed share count
- `price`: user-facing reference price passed into the order
- `execution_price`: execution price after slippage adjustment
- `amount`: gross turnover before fees
- In `/positions/trades`, `amount` is expressed in yuan.
- `commission`
- `stamp_tax`
- `slippage_amount`
- `net_amount`: final cash outflow for buys or cash inflow for sells after costs
- `trade_time`: execution timestamp

Pagination response fields:

- `orders`: current page detail rows
- `count`: row count of the current page
- `page`
- `size`
- `total`: total row count under the current filter
- `summary`: aggregate statistics under the current filter, not just the current page

These pagination fields are inside `data`, not top-level response keys.

`/positions/trades` `summary` fields:

- `order_count`
- `buy_count`
- `sell_count`
- `total_commission`
- `total_slippage_amount`
- `total_stamp_tax`
- `total_buy_amount`
- `total_sell_amount`
- `total_buy_net_amount`
- `total_sell_net_amount`
- `net_buy_amount`
- `net_sell_amount`

### Behavior Rules

- Position data is isolated by token. An agent can only access holdings under its own token.
- Current holdings are stored in `position`; historical executions are stored in `trade_order`.
- The skill interface does not support direct `PUT` or `DELETE` on holdings. Use buy or sell actions only.
- Buy actions are blocked on limit-up days. Sell actions are blocked on limit-down days.
- Trades are accepted only during exchange sessions: `09:15-09:25`, `09:30-11:30`, `13:00-15:00`.
- Orders outside trading sessions are currently rejected. The backend does not queue pending orders yet.
- Buy orders must be in round lots of 100 shares. `688.*` 科创板 buy orders must be at least 200 shares and still in 100-share increments.
- Beijing Stock Exchange is an exception to the 100-share round-lot rule above.
- Beijing Stock Exchange reference rules:
  - `8*.BJ` buy orders start at 100 shares and may increase in 1-share increments.
  - Single-order buy quantity on the Beijing Stock Exchange should not exceed 1,000,000 shares.
  - If a remaining sellable position is below 100 shares, it should be sold in one order.
  - When the user submits a buy order for an `8*.BJ` stock, apply the exchange reference rules above on the agent side and warn the user that backend BJ-specific enforcement may not be complete.
  - The current backend lot-size validator is explicitly verified for standard A-share round lots and `688.*` STAR Market rules; BJ-specific validation should be treated as partially verified unless it has been tested separately.
- Beijing Stock Exchange block-trade thresholds, such as 100,000 shares or RMB 1,000,000 minimum consideration, are exchange reference rules only and are outside the current skill interface for regular position trading.
- Sell orders may use odd lots, but are still subject to T+1 and trading-session rules.
- T+1 applies: shares bought today cannot be sold today. The backend enforces this from `trade_order` execution records.
- Buy orders are also capped by liquidity: order amount must not exceed `1%` of that stock's成交额 on the previous trading day.
- The liquidity cap uses the previous trading day's成交额 `amount`, not成交量 `vol`.
- In the source K-line table, `amount` is stored in `万元`; the backend converts it to yuan before evaluating the cap.
- The buy order amount used for the cap comparison is also in yuan.
- If the previous trading day is missing or `amount=0`, the backend rejects the buy order instead of inferring a fallback limit.
- The `1%` cap is evaluated per submitted buy order.
- Multiple buy orders for the same stock on the same day are each evaluated independently against the cap.
- Suspended or non-tradable stocks are rejected when realtime quotes indicate no executable market.
- Selling can be full or partial. Full sell removes the holding from current positions; partial sell decreases `qty`.
- `POST /positions/refresh` recomputes PnL from current quotes and returns the result, but does not write back the latest price into the position table.
- Position responses may include `quote_source=realtime`, `quote_source=last_close`, or `quote_source=cost_fallback`.
- If realtime quotes are missing on non-trading days or stale sessions, `last_close` means the API used the most recent trading day's close price for valuation.
- If neither realtime quotes nor latest close is available, `cost_fallback` means the API used `cost_price` as the current price fallback.
- This means portfolio PnL can still be queried on weekends or holidays; the valuation basis will be `last_close` instead of realtime.
- If realtime quotes are missing during refresh, the response includes `missing_quotes`.
- Position PnL includes transaction costs: buy commission, sell commission, sell stamp tax, and bilateral slippage.
- `market_value` should be interpreted as estimated net liquidation value after sell-side costs, not just `qty * current_price`.
- `market_value` is the per-position net liquidation estimate after sell-side costs.
- Trade order responses include execution-level fields such as `execution_price`, `commission`, `stamp_tax`, `slippage_amount`, and `net_amount`.
- `GET /positions` and `POST /positions/refresh` include per-position cost fields such as `buy_amount_gross`, `buy_commission`, `buy_cash_out`, `sell_commission`, `stamp_tax`, `market_value`, `profit_loss`, and `profit_rate`.
- `GET /positions`, `GET /positions/summary`, and `POST /positions/refresh` include summary cost fields such as `total_buy_amount_gross`, `total_buy_commission`, `total_market_value_gross`, `total_sell_commission`, `total_stamp_tax`, `total_cost`, `total_fee_cost`, `total_profit_loss`, and `total_profit_rate`.
- In position summary:
  - `total_cost` means total buy-side net cash out for current holdings
  - `total_fee_cost` means realized buy commission plus estimated sell-side commission and stamp tax on current holdings
  - `total_value` means estimated net liquidation value after current sell-side costs
  - `total_value` is the portfolio-level aggregate of per-position net values; do not confuse it with one position's `market_value`

### Agent Output Guidance

- If the user asks for current holdings, prefer `GET /positions`.
- If the user asks for portfolio summary, prefer `GET /positions/summary`.
- If the user asks for buy/sell history, prefer `GET /positions/trades`.
- If the user asks to refresh PnL, call `POST /positions/refresh`.
- When explaining PnL, mention `last_close` or `cost_fallback` if they appear, so the user does not mistake fallback pricing for realtime pricing.
