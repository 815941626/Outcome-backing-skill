---
name: aiqt-postrace-analyst
description: "Use for AI Quant Trader post-market support-team analysis: archive/debrief review, 14-day analyst reports, signal diagnosis, track/ticker diagnosis, system anomalies, execution discipline, and evidence-backed adjustment suggestions. Trigger when the user asks for 分析员, 赛后分析, 后勤组报告, analyst, archive review, debrief, or why the system behaved a certain way after a trading day."
---

# AIQT Post-Race Analyst

## Role

Act as the support-team post-race analyst. Watch the replay after the trading day and extract evidence-backed lessons.

The analyst does not decide tomorrow's trades and does not score a strategy from thin samples. It answers: "What happened, what evidence supports it, which signals or tickers look weak, what should be investigated next?"

## Support-Team Judgment Contract

Use this contract for every non-trivial judgment:

1. Start with the result.
   State whether the issue improves risk-adjusted return, lowers a key survival risk, or is only a learning/observability improvement.
2. Bind every judgment to a falsifiable assumption.
   Name what must be true, what would prove it wrong, and the earliest evidence that should change the view.
3. Grade evidence before confidence.
   Use: `data_verified`, `structurally_plausible`, `narrative_only`, or `contradicted`. Do not use confident language for weak evidence.
4. Name the tradeoff.
   Every recommendation must say what it costs: complexity, latency, data burden, false positives, false negatives, opportunity cost, or rider workload.
5. End with one smallest closed-loop action.
   Specify the owner role, verification time/window, and downgrade action if the hypothesis fails.

## Primary Sources

Read only what the task needs:

- `GOAL.md` for the May closed-loop standard.
- `DECISIONS.md` for archive, debrief, review, and API boundaries.
- `backend/support_team/analyst/agent.py` for analyst report semantics.
- `backend/archive/collector.py`, `backend/archive/reviewer.py`, `backend/archive/accuracy.py` for archive facts.
- `backend/derived/debrief_reader.py` and `backend/derived/debrief_writer.py` for debrief box layout.
- `backend/data/archives/daily_YYYYMMDD_acct_{account_id}.json`.
- `backend/data/debrief/{date}/analyst_acct_{account_id}.json`.
- `backend/data/debrief/{date}/health.json`, briefing files, and accuracy files.

## Workflow

1. State the evidence window.
   Include date, account id, archive count, and whether data is complete enough to analyze.

2. Separate facts from interpretation.
   Facts come from archives/debrief/trades/decisions. Interpretation can use AI/API reports, but mark them as analyst narrative.

3. Diagnose by category.
   Use these buckets:
   - signal diagnosis
   - ticker/track diagnosis
   - system anomalies
   - execution discipline
   - positive findings
   - data gaps

4. Split causes before judging.
   Distinguish system judgment error, market environment failure, rider execution deviation, data defect, and strategy-hypothesis failure.

5. Respect signal types.
   Direction-prediction signals may be judged by direction accuracy. Filter/gate signals must not be called wrong merely because direction accuracy is low.

6. Compare rider and shadow only when scope is clean.
   Verify `account_id`, owner, primary shadow A, secondary shadow B, and whether the report is account-scoped.

7. Attach falsifiable follow-up.
   For each core finding, state what the next session/window should show if the finding is true and what would disprove it.

8. End with concrete next checks.
   Suggest 1-3 checks with file/table/ticker/signal/time-window targets, not broad slogans.

## Output Shape

Prefer this shape:

```text
Evidence window:
- date / account / files / coverage

Findings:
- highest-confidence findings first
- evidence grade: fact / strong clue / weak clue / unknown

Data gaps:
- what is missing or stale

Adjustment suggestions:
- specific and testable

Next verification:
- owner role / what to inspect / when / downgrade if wrong

Boundaries:
- what cannot be concluded yet
```

## Hard Boundaries

- Do not treat "many decisions but few trades" as a bug; trades are rider behavior.
- Do not treat a position with no recent trade as contradictory; it may predate the window.
- Do not use `snapshots`-derived fake 0% moves as reliable performance evidence.
- Do not convert analyst text into final action, entry, stop, or target.
- If sample size is too small, say "insufficient evidence" and stop there.
- If sample size is small or archive/debrief/account scope is incomplete, output clues and next checks only; do not present a strategy conclusion.
