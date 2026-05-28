# StockPillar Reference Data

Per-endpoint deep reference for the shareholder/ownership/pledge/repurchase/block-trade family.
Covers exact field names, date-filter conventions, and per-endpoint output rendering rules.

For natural-language → endpoint trigger words, see
[general-rules.md](general-rules.md). For cross-endpoint interpretation rules (concentration vs
dispersion, pledge ratio risk thresholds, planned vs executed repurchases), see the
"Ownership, Capital, Pledges" section of [financial-statements.md](financial-statements.md).

Semantic boundary (keep these straight before reading endpoint rules):

- `holder-trades` is disclosure-driven ownership change.
- `block-trades` is negotiated transaction flow between counterparties.
- `repurchases` is company capital action progress.
- `ownership` is shareholder structure, not market turnover.
- `pledge` is share-pledge risk and release state, not funding flow.

## Endpoint Rules

### `/stocks/{ts_code}/events/holder-trades`

Use when:

- the user asks who increased or reduced holdings
- the user asks whether major shareholders or executives are selling
- the user wants change volume, ratio, or average transaction price

Exact-date filter:

- prefer `ann_date`
- `trade_date` may be used as an alias when the user only says "当天公告"

Key fields:

- `holder_name`
- `holder_type`
- `in_de`
- `change_vol`
- `change_ratio`
- `after_share`
- `after_ratio`
- `avg_price`

Output guidance:

- state whether the row is `增持` or `减持`
- distinguish announced disclosure date from transaction window `begin_date` and `close_date`
- when multiple rows exist, summarize the net direction first

### `/stocks/{ts_code}/events/block-trades`

Use when:

- the user asks about block trades, discount trades, or counterparties
- the user wants price, volume, amount, buyer, or seller

Date filter:

- exact day uses `trade_date`
- range uses `start_date` and `end_date`

Key fields:

- `price`
- `vol`
- `amount`
- `buyer`
- `seller`

Output guidance:

- mention the exact `trade_date`
- if the user is asking about unusual activity, describe the counterparties when available
- do not confuse block-trade records with secondary-market moneyflow

### `/stocks/{ts_code}/events/repurchases`

Use when:

- the user asks whether the company announced or executed repurchases
- the user wants repurchase progress, planned amount, or price band

Exact-date filter:

- prefer `ann_date`
- `trade_date` may be used as an alias for same-day disclosure questions

Key fields:

- `proc`
- `vol`
- `amount`
- `high_limit`
- `low_limit`
- `exp_date`

Output guidance:

- lead with current `proc`
- mention the execution or plan amount when present
- distinguish announcement date `ann_date` from expiration date `exp_date`

### `/stocks/{ts_code}/ownership/holder-numbers`

Use when:

- the user asks whether shareholder count is rising or falling
- the user wants a rough proxy for concentration or dispersion

Exact-date filter:

- prefer `ann_date`
- use `start_date` and `end_date` for a trend window

Key fields:

- `holder_num`
- `ann_date`
- `end_date`

Output guidance:

- explain whether shareholder count is increasing or decreasing across the requested window
- do not equate shareholder count directly with institutional conviction without caveat

### `/stocks/{ts_code}/ownership/top10-holders`

Use when:

- the user asks who the top shareholders are
- the user wants the latest ownership structure or historical changes

Exact-date filter:

- prefer `ann_date`
- use `start_date` and `end_date` for disclosure windows

Key fields:

- `holder_name`
- `hold_amount`
- `hold_ratio`
- `hold_float_ratio`
- `hold_change`
- `holder_type`
- `end_date`

Output guidance:

- group interpretation by one `ann_date` snapshot
- mention concentration if total `hold_ratio` is high
- do not mix rows from different `ann_date` snapshots without saying so

### `/stocks/{ts_code}/ownership/top10-floatholders`

Use when:

- the user asks specifically about float holders or tradable-float structure
- the user wants to know whether the float is concentrated

Interpretation rule:

- same semantics as top10 holders, but scoped to float holders

### `/stocks/{ts_code}/pledges/detail`

Use when:

- the user asks who pledged shares, whether they were released, or whether it is buyback-style pledge
- the user wants a detailed timeline

Exact-date filter:

- prefer `ann_date`
- `trade_date` may be used as an alias for same-day disclosure questions

Key fields:

- `holder_name`
- `pledge_amount`
- `start_date`
- `end_date`
- `is_release`
- `release_date`
- `pledgor`
- `p_total_ratio`
- `h_total_ratio`
- `is_buyback`

Output guidance:

- distinguish disclosed date `ann_date` from pledge start and end dates
- mention release status explicitly
- surface ratios when the user is asking about risk, not just raw amounts

### `/stocks/{ts_code}/pledges/stat`

Use when:

- the user asks for pledge ratio, number of pledge records, or high-level pledge risk
- the user wants one summary row per report date

Date filter:

- exact snapshot uses `trade_date` as the alias for `end_date`
- range uses `start_date` and `end_date`

Key fields:

- `pledge_count`
- `unrest_pledge`
- `rest_pledge`
- `total_share`
- `pledge_ratio`

Output guidance:

- lead with `pledge_ratio`
- mention whether the summary is a snapshot on `end_date`
- if there are multiple rows, compare the latest row with the previous one instead of free-form narrating every row

### `/stocks/{ts_code}/ownership/overview`

Use when:

- the user wants one-call context before deeper analysis
- the user asks broad questions such as "这个票股东结构怎么样" or "有没有质押和回购压力"

Response shape:

- `latest_holder_number`
- `latest_pledge_stat`
- `latest_top10_holders`
- `latest_top10_floatholders`
- `recent_holder_trades`
- `recent_block_trades`
- `recent_repurchases`
- `recent_pledge_details`

Output guidance:

- start from latest structural snapshot, then mention recent event-like changes
- if `latest_top10_*` exists, use its aggregated `holder_count` and `total_hold_ratio`
- absence of one subsection means no matched local rows in the requested range, not a proof that the event never existed
