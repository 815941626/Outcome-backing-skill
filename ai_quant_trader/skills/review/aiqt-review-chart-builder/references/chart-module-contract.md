# Review Chart Module Contract

Use this contract when creating a new AIQT review chart. Fill it before writing UI code.

## 1. Chart Identity

```yaml
chart_id:
title:
review_question:
owner_surface:
```

`review_question` must be outcome-bound. Example:

```text
When rotation_score is high, does low_defensive outperform high_growth over T+3?
```

## 2. Frozen Snapshot Contract

Required fields:

```yaml
date:
session_time:
source_version:
signal_label:
signal_score:
confidence:
frozen_evidence:
expected_effect:
invalidation_rule:
action_hint:
data_quality:
```

Rules:

- Save the snapshot at judgment time.
- Keep enough evidence to explain the score without reconstructing the past.
- Do not rewrite frozen fields after the fact.
- Mark missing or stale data explicitly.

## 3. Outcome Contract

Required fields:

```yaml
outcome_window: T+1 | T+3 | T+5
outcome_timestamp:
high_basket_return:
low_basket_return:
realized_spread:
trade_action_taken:
avoided_action_result:
calibration_bucket:
review_flag:
```

Rules:

- Append outcomes when the window completes.
- Store multiple windows separately.
- Keep realized market behavior separate from realized trade PnL.
- Label the sample type: real trade, shadow, manual, LLM probe, or background-only.

## 4. Axis Contract

For each axis:

```yaml
axis_name:
formula:
direction:
neutral_band:
missing_data_behavior:
```

Example:

```yaml
x_axis:
  axis_name: rotation_score
  formula: high_unwind_score + low_absorb_score + spread_flip_score
  direction: higher means stronger high-to-low rotation expectation
  neutral_band: [-20, 20]
  missing_data_behavior: mark no-clear-signal
```

## 5. Quadrant or Bucket Semantics

Define every visible region:

```yaml
regions:
  right_up:
    meaning:
    default_action:
    review_priority:
  right_down:
    meaning:
    default_action:
    review_priority:
  left_down:
    meaning:
    default_action:
    review_priority:
  left_up:
    meaning:
    default_action:
    review_priority:
  center:
    meaning:
    default_action:
    review_priority:
```

Do not label a region as "good" or "bad" without stating what system behavior it validates or invalidates.

## 6. Calibration Curve

If adding a curve, define:

```yaml
bucket_method:
min_samples_per_bucket:
y_metric:
expected_shape:
failure_shape:
```

Example:

```text
Expected shape: higher rotation_score buckets should show higher median realized_spread.
Failure shape: flat or negative slope after enough samples.
```

## 7. Storage Contract

Specify:

```yaml
storage_kind: sqlite | jsonl | existing_project_table
path_or_table:
primary_key:
upsert_policy:
retention:
```

Preferred rule:

```text
Use append-only snapshots plus outcome updates keyed by chart_id/date/outcome_window.
```

## 8. Review Flags

Default flags:

```text
high_confidence_false_positive
high_confidence_missed_signal
data_quality_gap
action_value_unclear
sample_too_small
```

Only high-priority flags should create human-review work. Ordinary center-band samples stay background-only.

## 9. Proof Boundary

Before presenting conclusions, classify evidence:

```text
visual_only
directionally_plausible
calibrated_signal
action_value_supported
tradable_edge_supported
```

Most new charts start at `visual_only` or `directionally_plausible`. Do not upgrade without enough samples and an action-value metric.

## 10. Render Contract

If the user asks for the chart to exist in the product, define:

```yaml
render_surface:
  frontend_file:
  api_endpoint:
  chart_type:
  controls:
  loading_state:
  error_state:
  empty_state:
  save_snapshot_action:
```

Minimum visible pieces:

```text
primary chart
sample count
evidence level
latest frozen point
quadrant counts
calibration buckets
limitations or stale-data warning
```

For a 4-quadrant chart, the HTML/SVG must show:

```text
x zero/neutral band
y zero line
point colors by quadrant
hover/title with date, score, spread, label
```

Do not finish with only a JSON endpoint unless the user explicitly asked for backend-only data.
