# StockPillar Supply Chain Reference

Use this reference with `../SKILL.md` when the user asks about AI supply-chain graphs, company exposure, candidate review queues, or event propagation.

## Agent Decision Shortcut

Follow this shortcut before reading endpoint details:

- "AI 供应链五层图谱 / 图谱结构 / 有哪些层" -> `GET /themes/{theme_code}/supply-chain/graph`.
- "某一层/某个环节影响哪些公司" -> `GET /themes/{theme_code}/supply-chain/exposures`.
- "今天/某天 AI 供应链影响了哪些公司/股票" -> `GET /themes/{theme_code}/supply-chain/impacts`.
- "某条事件如何传导到公司/股票" -> `GET /events/{event_id}/supply-chain-impact`.
- "某只股票在供应链哪里/上下游是谁" -> `GET /stocks/{ts_code}/supply-chain`.
- "新发现的供应链公司对应哪些A股" -> `GET /themes/{theme_code}/supply-chain/a-share-candidates/search`.
- "哪些关系待审核/AI 抽取了什么关系" -> `GET /themes/{theme_code}/supply-chain/candidates`.
- "审核/通过/驳回/禁用/同步/提升候选关系" -> explain that these are handled by the review page or scheduled pipeline; do not route to POST endpoints from this skill.
- "重新跑传导/重建向量/同步暴露" -> explain that these are maintenance operations handled outside normal agent routing.

Default strategy:

- Use `theme_code=AI_EMBODIED` for AI supply-chain requests unless the user names another theme.
- Prefer approved graph and exposure data by default.
- Include pending or inactive records only for audit/review tasks.
- Treat the graph as global. Do not filter out NVIDIA, TSMC, Microsoft, AWS, OpenAI, SK hynix, or other non-A-share companies.
- Supply-chain POST maintenance endpoints are intentionally not exposed to ordinary agents. Use read-only endpoints and direct the user to the review page or scheduled pipeline for mutations.

## When To Use

Use these endpoints when the user asks:

- AI 产业链或供应链图谱有哪些层级、节点、公司
- 某个事件如何沿供应链传导到公司或股票
- 某个环节影响哪些公司
- 新发现的供应链公司、产品线、新闻文本可能对应哪些 A 股上市公司
- 某只股票处在供应链哪一层、上下游是谁
- 哪些供应链关系或公司暴露需要查看或人工复核

Current first theme for the AI supply-chain graph is `AI_EMBODIED`.

## Endpoint Choice

- `GET /themes/{theme_code}/supply-chain/graph`: first choice for drawing or explaining the theme supply-chain graph. It returns `layers`, `nodes`, `edges`, and `exposure_edges`.
- `GET /themes/{theme_code}/supply-chain/exposures`: first choice for answering "某一层/某个环节影响哪些公司". It is the reviewed segment-to-company pool. It supports `chain_code`, `segment_node_id`, `company_node_id`, and `review_status` filters. Use `data.records` as the list. Rows include resolved segment/company names and security fields such as `ts_code`, `stock_name`, `market`, `securities`, and `is_a_share`. If the persisted exposure table is empty, the endpoint may return read-only derived records from approved graph edges with `source=derived_from_graph_edges` and `needs_sync=true`.
- `GET /themes/{theme_code}/supply-chain/candidates`: use for review queues and AI-extracted relations before they become official graph edges. Manual approval now attempts immediate graph promotion; invalid long-term graph relations are moved to `rejected` with a `system_rejected:*` reviewer note.
- `GET /themes/{theme_code}/supply-chain/a-share-candidates/search`: use for read-only A-share candidate resolution when a newly discovered supply-chain company may correspond to one or more A-share listed companies. It searches Chroma collection `stockpillar_a_share_companies_v4_1024` and returns TopK candidates with `vector_score`, `name_match_score`, `final_score`, and `match_reasons`. Do not treat the result as approved graph data until a relation is promoted or reviewed.
- `GET /themes/{theme_code}/supply-chain/impacts`: first choice for date-level supply-chain propagation summaries such as "今天 AI 供应链影响哪些公司" or "今日供应链传导覆盖率". Use `trade_date=YYYYMMDD` or `start_time/end_time`. It returns `coverage.theme_event_count`, `coverage.processed_event_count`, `coverage.impact_event_count`, event-level `records`, and aggregated `impact_on_a_shares` / `impact_on_securities` for the current page.
- `GET /stocks/{ts_code}/supply-chain`: use for one listed stock's supply-chain position.
- `GET /events/{event_id}/supply-chain-impact`: use for persisted propagation results after an event has been processed. Prefer `impact_on_a_shares` when the user asks which A-share companies are affected. The response resolves securities from direct company nodes, direct segment exposures, and lower-confidence related same-chain segment exposures.
- `GET /themes/{theme_code}/supply-chain/prefilter-events`: use to inspect which theme events are relevant enough to enter extraction.

## Parameters

- `theme_code`: required path variable. Use `AI_EMBODIED` unless the user names another theme.
- `chain_code`: optional graph selector. Omit it unless the user asks for a specific supply chain.
- `layer_index`: optional integer for graph layer filtering.
- `include_pending=true`: include unapproved graph edges. Do not use by default.
- `include_inactive=true`: include disabled graph records. Use only for audits.
- `review_status`: candidate/exposure filter. Common values are `pending`, `auto_approved`, `approved`, and `rejected`.
- `segment_node_id` and `company_node_id`: filters for exposure records.
- `query`: required query field for A-share vector candidate search. It can be a company name, English name, product text, or news sentence.
- `top_k` and `min_score`: optional A-share vector candidate search controls.
- `trade_date`, `start_time`, and `end_time`: date filters for theme-level supply-chain impacts. Prefer `trade_date=YYYYMMDD` for daily summaries.
- `source_event_id` or `event_id`: filters candidate relations or persisted event impact reads.

## Important Fields

- Graph `layers` describe the five-layer structure. Use `layer_index`, `name`, and `description` to explain the hierarchy.
- Graph `nodes` include conceptual nodes, product/technology nodes, and company nodes. Company nodes may be global, not A-share-only.
- Graph `edges` are reviewed supply-chain relations such as `supplier_to`, `customer_of`, `product_of`, `component_of`, `depends_on`, `benefits_from`, `risk_from`, `competitor_of`, `substitute_for`, and `technology_support`.
- Graph `exposure_edges` are derived or reviewed "segment/product/technology -> company" impact edges. Use these when translating a layer or concept into impacted companies.
- Candidate rows include extracted entities, `relation_type`, evidence text, confidence, source event metadata, and `review_status`.
- Exposure rows include segment node, company node, exposure type, confidence, source relation, review status, resolved `segment_name`, `company_name`, `ts_code`, `stock_name`, `market`, `securities`, and `is_a_share`. The exposure list also returns `source`, `persisted`, and `needs_sync` so agents can tell whether data came from the stored exposure table or a read-only graph-edge fallback.
- A-share candidate search rows include `ts_code`, `stock_name`, `industry`, `industry_a30`, `vector_score`, `name_match_score`, `final_score`, `match_reasons`, and any existing supply-chain segments from the exposure index. These rows are candidates only.
- Prefilter responses include `source_total`, `raw_scored_total`, `deduped_total`, `selected_total`, and `items`. The prefilter removes duplicate titles before extraction and downranks hard noise such as market sentiment roundups, financing-balance/ETF flows, routine regulatory disclosure issues, and broad macro-loan news.
- Event impact rows include event id, theme, target node/company/security, path depth, path score, and trace path when available.
- Event impact responses include `impact_on_securities` and `impact_on_a_shares`. Use `impact_on_a_shares` for A-share answers, and only fall back to raw node records when there is no security mapping. `resolution_scope=direct_segment` means the event hit the exact segment exposure; `resolution_scope=related_segment` means the system expanded from an abstract node to same-chain/same-role exposure segments with a lower multiplier.
- Theme impact responses include `coverage`. If `coverage.pending_event_count` is high or `processed_event_count` is much lower than `theme_event_count`, explicitly say the daily propagation pipeline is still catching up instead of claiming there are no supply-chain impacts.

## Interpretation Rules

- Do not treat the graph as A-share-only. Global upstream nodes such as NVIDIA, TSMC, SK hynix, Microsoft, AWS, and OpenAI can be legitimate event sources.
- When the user asks "这个事件影响哪些公司", use persisted `/events/{event_id}/supply-chain-impact`. Read `impact_on_a_shares` first for A-share output. If it is empty, say the event has no persisted propagation result yet or the pipeline has not processed it; do not run mutation endpoints from this skill.
- When the user asks "今天 AI 供应链影响哪些公司/股票", use `/themes/{theme_code}/supply-chain/impacts?trade_date=YYYYMMDD` first. Do not infer 0 impact from `/themes/{theme_code}/events`; check `coverage` and persisted impact records.
- When the user asks "这个环节影响哪些公司", prefer `/supply-chain/exposures` over raw graph edges.
- When the user asks "新闻里出现的新公司如何映射到A股", use `/supply-chain/a-share-candidates/search` first. Return candidates and scores; do not claim a final mapping unless confidence is high and there is supporting evidence.
- During backend candidate promotion, newly discovered companies are checked against the A-share vector index before any new company node is created. Ambiguous matches stay out of the official graph with candidate notes instead of being blindly persisted.
- When explaining propagation, distinguish official graph relations, candidate relations, and exposure edges.
- When an event hits an abstract segment such as GPU/GPGPU, affected A-share companies may appear through `related_segment` exposure resolution. Explain this as "同链路/同角色环节穿透", not as a direct supplier relationship.
- If `/supply-chain/exposures` returns `needs_sync=true`, the answer may use the derived records, but mention that the scheduled pipeline or maintenance UI should sync the persisted exposure table before treating the data as fully materialized.
- Treat confidence as evidence quality, not expected stock return.
- If a company is global or unlisted, do not force it into an A-share code. Use stock mappings only when the API returns them.
- For manual correction, direct the user to the supply-chain review page rather than calling mutation endpoints.
- `segment_code` values referenced in supply-chain exposures (`AI_CHIP`, `OPTICAL_CPO`, `PCB`,
  `MEMORY_ADV_PACKAGING`, `AIDC_POWER_COOLING`, `IDC_CLOUD`, `SEMI_BASE`, `AI_SOFTWARE`,
  `AI_APPLICATION`, `AIGC_CONTENT`, `ROBOTICS_EMBODIED`, `EDGE_AI_IOT`, `DATA_TOOLCHAIN`,
  `WEAK_CONCEPT`, `OTHER`) share the same canonical enum as `/themes/{theme_code}/stock-pool`.
  When the user asks "光模块段在主题池里有哪些股", chain
  `/supply-chain/exposures?chain_code=...&segment_node_id=...` (公司暴露) →
  `/themes/{theme_code}/stock-pool?segment_code=OPTICAL_CPO` (committed pool 中的 A 股标的)
  rather than re-mapping segment names yourself. See
  [industries-events.md `/themes/{theme_code}/stock-pool` Guide](industries-events.md) for the
  full enum and per-segment commitment level.

## Example Calls

```bash
curl -G "$STOCKPILLAR_API_URL/themes/AI_EMBODIED/supply-chain/graph" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "layer_index=1"
```

```bash
curl -G "$STOCKPILLAR_API_URL/themes/AI_EMBODIED/supply-chain/exposures" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "chain_code=compute_chip" \
  --data-urlencode "review_status=approved" \
  --data-urlencode "size=100"
```

```bash
curl -G "$STOCKPILLAR_API_URL/themes/AI_EMBODIED/supply-chain/a-share-candidates/search" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "query=海光DCU适配DeepSeek大模型" \
  --data-urlencode "top_k=10"
```

```bash
curl -G "$STOCKPILLAR_API_URL/events/12345/supply-chain-impact" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "theme_code=AI_EMBODIED" \
  --data-urlencode "limit=100"
```

```bash
curl -G "$STOCKPILLAR_API_URL/themes/AI_EMBODIED/supply-chain/impacts" \
  -H "Authorization: Bearer $STOCKPILLAR_API_KEY" \
  --data-urlencode "trade_date=20260425" \
  --data-urlencode "size=50"
```
