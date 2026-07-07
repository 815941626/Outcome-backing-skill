---
name: aiqt-review-loop
description: >-
  Use for AI Quant Trader closed-loop post-market review and debrief orchestration:
  deciding what must be reviewed after a trading day, checking whether cloud/local
  review data is complete, separating real/shadow/LLM/manual samples, reading
  judgment anchors, preflight traces, trades, closed-loop summaries, behavior
  profiles, thesis evidence, archive/debrief files, and producing concise attribution
  plus 1-3 next iteration actions. Trigger when the user asks 复盘, 闭环复盘,
  赛后归因, 云端数据 pull 后怎么看, 哪些票该人读, 静态尺子复盘, 影子马复盘,
  有交易/没交易为什么, R倍数, attribution, debrief, archive review, or whether
  review data is missing/redundant.
---

# AIQT Review Loop

Use this skill to keep AI Quant Trader review work on the main axis:

```text
三大信息源 -> 走势判断 -> 执行/未执行 -> 结果/R倍数 -> 归因 -> 算法迭代
```

The job is not to read everything. The job is to decide which facts matter, which samples need human review, what can be concluded, what is still missing, and which small change should improve the next loop.

## Core Rule

Start every non-trivial review by answering:

1. What result or judgment is being reviewed?
2. What was the frozen ruler at decision time?
3. Did the system act, not act, or only observe?
4. What happened afterward?
5. Is the outcome attributable to system judgment, data, execution, rider override, market regime, or insufficient evidence?
6. What is the smallest next change or check?

Keep review-only evidence out of execution logic unless the user explicitly asks for an implementation change and the safety boundary is clear.

## Data Completeness Gate

Before interpreting, check whether the review window is complete enough.

Minimum facts:

- `date` / market session / whether the day is complete.
- `account_id`, account type, and whether the sample is real, shadow A/B, LLM probe, manual, static-reference, or historical import.
- Price path after the judgment: current, high, low, close, T+1/T+3/T+5 when available.
- Decision evidence: three-board evidence, `judgment_anchors`, thesis, behavior profile, LLM cognition if enabled.
- Canonical decision brief: `decision_brief` payload and `decision_brief_snapshots` rows, including one-line verdict, buy/hold/abandon conditions, current blocker, evidence grade, and data-quality state.
- Execution evidence: today-action, preflight trace, trade record, position state, sell/exit record, R multiple if closed.
- Review evidence: archive, debrief, `closed_loop_summary`, attribution payloads, anomaly queue.

If these are missing, classify the gap before judging the strategy:

```text
missing_at_source: source data was never recorded
missing_in_pull: cloud/local sync did not fetch it
missing_join: data exists but is not linked by ticker/date/account/decision_id
stale_snapshot: data exists but is not fresh enough
redundant_noise: data exists but is too repetitive for human review
```

## Primary Repo Surfaces

Read only what the task needs, but prefer these surfaces:

- `GOAL.md`: target and credibility boundary.
- `DECISIONS.md`: durable system behavior and review boundaries.
- `backend/closed_loop_router.py`: closed-loop review output.
- `backend/decision/judgment_anchor_attribution.py`: static ruler attribution.
- `backend/decision/decision_brief.py`: canonical one-line rider verdict and review snapshot storage.
- `GET /api/advice-center/decision-briefs?ticker=...&days=...`: recent decision-brief snapshots for closed-loop review.
- `backend/live_trace.py`: preflight/manual-trade evidence.
- `backend/performance/trade_review.py`: trade attribution and R/result semantics.
- `backend/strategy_origin.py`: formal/manual/LLM/static-reference source separation.
- `backend/archive/collector.py`, `backend/archive/reviewer.py`, `backend/archive/accuracy.py`: archive facts.
- `backend/derived/debrief_reader.py`, `backend/derived/debrief_writer.py`: debrief layout and legacy compatibility.
- `backend/fundamental/behavior_profile.py`: stock behavior habit evidence.
- `backend/data/archives/daily_YYYYMMDD_acct_{account_id}.json`: account-scoped archive.
- `backend/data/debrief/{date}/...`: debrief outputs; verify account scope before trusting legacy paths.

## Sample Selection

Do not send every ticker to human review. Split samples first.

Human-readable P0 samples:

- Real trade opened, closed, or manually retagged.
- Position had a sell/reduce/hold decision with meaningful PnL or R movement.
- Static judgment anchor was active and price hit confirm/invalidation/target area.
- Today-action said buy/sell/reduce but preflight blocked, was missing, or rider deviated.
- A ticker triggered LLM cognition, behavior-profile habit, or thesis kill condition.
- Data anomaly: missing snapshot, stale source, account mismatch, duplicate archive, impossible price, missing execution trace.

Human-readable P1 samples:

- No trade, but price came close to entry/stop/target/invalidation.
- Shadow A/B disagreed materially.
- Strong news/fundamental/technical conflict.
- Watchlist ticker with repeated behavior-profile trigger.

Background-only samples:

- No position, no action change, no active anchor, no near-trigger, no anomaly.
- Repeated low-value snapshots with unchanged state.
- Tickers whose only change is ordinary price noise.

Always preserve counts for background samples, but do not put them into the human narrative unless they explain coverage.

## Review Order

Use this order to avoid mixing facts and opinions.

### 1. Evidence Window

State:

```text
date:
account:
market close status:
data surfaces checked:
coverage:
blocking data gaps:
```

If the data window is incomplete, stop strategy judgment and output only data-gap diagnosis plus next pull/fix steps.

### 2. Canonical Ruler

Find the frozen ruler:

- Static judgment anchor if available and active.
- Canonical `decision_brief` snapshot if available for the account/ticker/date.
- Preflight trace for real-account action.
- Today-action/advice snapshot for planned action.
- Thesis and behavior-profile evidence for fundamental context.
- LLM cognition only if the LLM review feature was enabled for that ticker/day.

If multiple rulers conflict, name the hierarchy:

```text
real preflight/trade truth > strategy_origin > active judgment anchor > today-action snapshot > thesis/behavior profile > analyst narrative
```

`decision_brief` is the canonical rider-facing synthesis, but it is not execution truth. Use it to ask "what did the system tell the rider in one sentence?" Then verify that statement against price path, triggers, and execution evidence.

### 3. Sample Type

Classify each relevant ticker:

```text
trade_executed
trade_blocked
manual_or_llm_probe
triggered_but_no_trade
near_trigger
hold_position_review
static_anchor_validation
behavior_profile_validation
decision_brief_validation
data_anomaly
background_stat_only
```

### 4. Outcome Measurement

Use the right measurement for the sample:

- Closed trade: realized PnL and R multiple.
- Open position: unrealized PnL, drawdown, distance to stop/target, current R proxy.
- No trade with active anchor: whether price moved toward confirm, target, invalidation, or stayed range-bound.
- Blocked trade: whether the block prevented loss, missed gain, or remains unknown.
- Behavior-profile habit: T+1/T+3 result against the pattern definition.
- LLM cognition: whether its trigger/abandon conditions were observable and followed.
- Decision brief: whether the one-line verdict, buy conditions, hold/sell management, abandon conditions, current blocker, and evidence grade matched the later price path and execution truth.

Do not judge a filter/gate by direction accuracy alone. A filter can be correct by preventing low-quality action.

### 5. Attribution

Use these cause buckets:

```text
system_judgment_error: the system read fundamentals/news/K-line wrong
execution_gap: the system had a valid plan but execution/preflight/trade link failed
rider_deviation: human action diverged from system or source was manual/LLM probe
data_defect: stale/missing/mixed-account data changed the judgment
market_regime_failure: setup was reasonable but environment shifted
strategy_hypothesis_failure: the playbook or behavior habit did not hold
insufficient_evidence: sample too small or data incomplete
correct_wait: no trade was the intended and validated action
```

Keep blocked preflight truth intact. If a human traded anyway, do not rewrite the blocked trace into permission.

## Static Ruler Rules

The static judgment anchor is the main ruler for走势判断. It can validate both trades and non-trades.

Review questions:

- Was the anchor canonical and active for the date?
- What was predicted: direction, range, confirm, invalidation, target?
- Did price hit confirm, target, invalidation, or stay inside the expected path?
- If no trade happened, was that because conditions did not trigger, preflight blocked, data was missing, or the system failed to create an executable plan?
- Should the result update the algorithm, the behavior profile, the thesis, or only the watchlist note?

Do not call "no trade" a failure unless the frozen ruler said a trade should have been possible and the execution path failed.

## Decision Brief Snapshot Rules

The decision brief is the system 1.0 V0 rider ruler. It is the first place to check whether many cards actually became one clear judgment.

Read from:

```text
payload["decision_brief"]
decision_brief_snapshots
GET /api/advice-center/decision-briefs?ticker=002340&days=14
```

Required fields for review:

```text
one_line
situation.label / situation.summary
can_buy_now.state / can_buy_now.reason
conditions.buy
conditions.hold_or_sell
conditions.abandon
supporting_evidence
opposing_evidence
current_blocker
evidence_grade
data_quality
layer_votes
review_contract.sample_type
brief_hash
```

Review questions:

- Did `one_line` correctly name the current market case?
- Did `can_buy_now` match the later path, or was it too strict/too loose?
- Were the buy conditions observable and did they trigger?
- Did the abandon conditions trigger, and did the system/rider respond?
- Was the current blocker the real blocker, or did another layer actually decide the outcome?
- Which layer was most useful: technical facts, current market case, big case, three-board, LLM, anchor, or execution boundary?
- Was this a data-quality problem, a synthesis problem, or an execution/rider problem?

Sample classification:

```text
decision_brief_action_candidate: brief allowed action after preflight
decision_brief_position_review: brief managed an existing position
decision_brief_stale_decision: brief blocked action due to missing fresh decision
decision_brief_market_case: brief only named the current tape/case
decision_brief_llm_review: brief included an LLM cognition sample
decision_brief_background: no trigger, keep count only unless anomalous
```

Do not score the brief as "wrong" merely because the stock later rose after a no-buy verdict. First check whether its stated buy conditions ever appeared, whether risk/reward was acceptable at that moment, and whether the blocker was a deliberate safety boundary.

## Less-Is-More Debrief

Human review should read like a judgment report, not a database dump.

Target shape:

```text
1. Data integrity: complete / incomplete / noisy
2. Top 3 reviewed samples
3. What the system got right
4. What the system got wrong or could not know
5. What data was missing or redundant
6. Next 1-3 actions
```

Prune:

- repeated unchanged ticker states
- raw snapshot rows without a decision consequence
- duplicate archive/debrief variants unless diagnosing sync/account bugs
- LLM or analyst prose that does not tie to an observable trigger

Keep:

- canonical decision briefs
- canonical anchors
- preflight traces
- strategy origin
- action changes
- trigger/near-trigger facts
- PnL/R after execution
- clear data anomalies

## Evidence Grades

Use one of these grades for every finding:

```text
data_verified: directly supported by stored facts
strong_clue: consistent across multiple sources but not fully closed
weak_clue: plausible but small sample or missing one link
insufficient_data: cannot judge yet
contradicted: available data says the claim is wrong
```

Never let confident wording outrun the evidence grade.

## Output Shape

Use this default structure:

```text
Evidence window:
- date / account / sources / coverage

Human-review queue:
- ticker / sample type / why it is included

Findings:
- highest-confidence findings first
- evidence grade
- facts first, interpretation second

Attribution:
- ticker / outcome / cause bucket / confidence

Data gaps and noise:
- missing source vs missing pull vs missing join vs redundant noise

Next iteration:
- 1-3 actions only
- owner lens
- acceptance check

Boundaries:
- what cannot be concluded yet
```

## Hard Boundaries

- Do not merge real-account PnL with formal system performance without `strategy_origin`.
- Do not treat LLM probes, manual trades, or static-reference trades as formal system trades.
- Do not treat "many decisions but few trades" as a bug by itself.
- Do not treat review-only behavior profiles or thesis evidence as execution permission.
- Do not change thresholds from one day of results.
- Do not bury missing data inside a strategy conclusion.
- Do not output more than 1-3 next actions unless the user explicitly asks for a backlog.
