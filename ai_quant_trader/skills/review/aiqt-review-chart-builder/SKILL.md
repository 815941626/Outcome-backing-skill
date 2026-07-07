---
name: aiqt-review-chart-builder
description: Use for AI Quant Trader modular review-chart design and implementation, especially when the user asks to build 4-quadrant review charts, expectation-vs-outcome curves, high-to-low rotation calibration charts, server-side snapshot storage, chart data contracts, or reusable chart modules for closed-loop trading review. Trigger on 复盘图表, 四象限, 复盘曲线, 高切低图, chart module, frozen expectation, outcome calibration, or modular review chart.
---

# AIQT Review Chart Builder

Use this skill to turn a trading-review idea into a reusable chart module. The chart is not decoration; it must answer whether a frozen system judgment later behaved inside its expected boundary.

## Core Outcome

Every review chart must connect:

```text
frozen judgment -> expected effect -> stored snapshot -> realized outcome -> calibration verdict
```

Do not build charts that only explain the market after the fact. A valid chart must make false confidence easier to see.

## Workflow

1. Pin the review question.
   State the judgment being calibrated, such as `high_to_low_rotation`, `market_risk_off`, `exit_bucket`, or `entry_filter`.

2. Define the frozen expectation.
   Write what the system believed at decision time and what later result would support or refute it. Avoid vague labels like "looked right".

3. Choose the chart pattern.
   - Use a 4-quadrant chart when comparing system score direction against realized direction.
   - Use a binned calibration curve when testing whether higher scores produce stronger outcomes.
   - Use a timeline when checking whether behavior changes after the signal.
   - Use a confusion table only when labels are discrete and the outcome window is fixed.

4. Define the data contract before UI work.
   Specify snapshot fields, realized outcome fields, storage path/table, freshness, and backfill rules. See `references/chart-module-contract.md`.

5. Produce a visible render surface when the user asks for a chart.
   If the user asks to "make the chart", "do the HTML", "draw it", or "show it in the app", deliver a real renderable surface, not only backend JSON. Prefer the host project's existing frontend stack. For simple dashboards, an inline SVG/HTML chart is acceptable and avoids new dependencies.

6. Keep action attribution separate.
   A chart can show that a signal contains information; it does not prove a trading edge unless it also connects to avoided loss, improved R, lower drawdown, or better execution discipline.

7. Add a no-trade interpretation.
   If the system's correct action was to reduce risk or avoid chasing, measure whether the avoided action was lower quality. Do not judge only by missed upside.

8. Design the failure review.
   Mark points that are high-confidence and wrong as human-review candidates. Do not send every ordinary noisy point to human review.

## 4-Quadrant Default

For high-to-low rotation review, prefer:

```text
X axis: rotation_score at snapshot time
Y axis: realized_spread over T+N

realized_spread = low_defensive_basket_return - high_growth_basket_return
```

Quadrants:

```text
right/up: system expected high-to-low rotation and it realized
right/down: false positive; review high-priority
left/down: correct non-rotation or growth-favored condition
left/up: missed high-to-low rotation; check missing factors
center band: no-clear-signal; do not force attribution
```

Use T+1, T+3, and T+5 windows by default. The first implementation may show one active window and keep the others as selectable tabs or filters.

## Storage Rules

Prefer server-side snapshots inside the project over local manual review files.

Minimum snapshot fields:

```text
date
session_time
chart_id
signal_label
signal_score
confidence
frozen_evidence
expected_effect
invalidation_rule
action_hint
data_quality
```

Minimum realized fields:

```text
outcome_window
high_basket_return
low_basket_return
realized_spread
trade_action_taken
avoided_action_result
calibration_bucket
review_flag
```

Do not overwrite the original snapshot when outcomes arrive. Append or update only outcome fields with an audit timestamp.

## Implementation Guidance

When implementing inside `ai_quant_trader`, reuse existing market-structure, decision snapshot, performance, and closed-loop surfaces before adding a new pipeline.

Recommended module shape:

```text
backend/review_charts/
  registry.py          # chart ids and chart specs
  snapshots.py         # freeze daily chart inputs
  outcomes.py          # fill T+1/T+3/T+5 outcomes
  serializers.py       # API-ready chart payloads
  charts/
    rotation_quadrant.py
```

Recommended data location:

```text
backend/data/review_charts.db
```

or an existing project database if the repo already has a clear review snapshot store.

## Frontend Rules

When adding a chart to an existing app:

- Reuse the app's current tab, fetch helper, styling tokens, and layout.
- Render at least the primary visual, summary metrics, and loading/error/empty states.
- Make the axis semantics visible through labels, not a separate essay.
- Keep neutral/no-signal samples visually distinct from validation/failure samples.
- Add controls only for meaningful chart dimensions, such as T window and lookback.
- Do not require a charting library for a simple quadrant or calibration curve; SVG is enough.
- If a save/freeze action exists, make it explicit and separate from read-only chart loading.

## Guardrails

- Do not call a chart proof of profit unless it is tied to PnL, R, drawdown, or avoided bad trades.
- Do not tune thresholds from one memorable day.
- Do not force every day into a quadrant; keep a neutral band.
- Do not mix real trades, shadow decisions, LLM probes, and manual actions without labels.
- Do not let chart modules change execution permissions directly. They can inform a later rule only after review.

## References

- `references/chart-module-contract.md`: reusable contract for new review chart modules.
