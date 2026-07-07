---
name: aiqt-hot-path-discipline
description: Use for AI Quant Trader work when the user mentions hot path, cold path, alpha, making money, missed buys, bad buys, buy/sell/entry/stop/sizing, today-actions action quality, or complains that Codex keeps adding review/audit/snapshot bureaucracy instead of improving trading decisions.
---

# AIQT Hot-Path Discipline

## Purpose

Keep AI Quant Trader work attached to improved risk-adjusted trading action. Do not let an alpha problem drift into cold-path bureaucracy.

Hot-path work improves or evaluates one of:

- buy vs no-buy outcome
- sell vs hold outcome
- entry price or entry anchor
- stop loss or invalidation point
- target or expected R
- planned shares or sizing
- missed upside, drawdown, realized/forward R
- first-screen action latency when it blocks the rider's decision

## Cold-Path Warning

If the proposed answer mainly adds Contract, Audit, Snapshot, Review, Sync, Task, dry-run, confirmation, dashboard, or observability layers, classify it as cold-path unless it directly prevents real-account danger, data loss, or a current hot-path decision failure.

## Workflow

1. Name the concrete trading problem.
2. Classify the request as `hot_path`, `outer_safety`, `review_feedback`, `ops_latency`, or `cold_path`.
3. If hot-path, require price-path evidence or an action comparison.
4. Prefer a change that affects entry/stop/target/sizing/action timing before adding meta layers.
5. Preserve outer safety boundaries: account isolation, real-account no-auto-order, max loss, broker/trade truth, and data-loss protection.
6. Reject inner hesitation expansion when the actual problem is alpha quality.

## Required Acceptance

A hot-path iteration must report at least one of:

- expected R
- realized or forward R
- missed upside
- drawdown avoided or caused
- action vs inaction comparison
- latency reduction on the rider-facing action surface

## Response Shape

```text
Trading problem:
Classification:
Why this is/is not hot-path:
Smallest useful action:
Evidence required:
Safety boundary preserved:
What is intentionally not built:
```
