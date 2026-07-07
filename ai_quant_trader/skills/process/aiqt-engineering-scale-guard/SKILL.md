---
name: aiqt-engineering-scale-guard
description: Use for AI Quant Trader architecture, refactor, endpoint design, today-actions boundary, action permission, managed trade plan, cloud/Mac deployment design, latency, or any proposal where Codex must choose implementation scale without overbuilding or bypassing modular-monolith boundaries.
---

# AIQT Engineering Scale Guard

## Purpose

Choose the smallest durable engineering shape for AI Quant Trader. Keep the system a modular monolith with explicit anti-corruption boundaries unless measured evidence proves that a heavier architecture is needed.

## Domain Shape

Preserve the four-module product shape:

- `market_structure`: regime and opportunity environment
- `stock_pool`: ticker attributes, lifecycle, and playbook fit
- `observation`: current ticker-state judgment and rider-facing action surface
- `review`: post-outcome attribution that feeds corrections upstream

## Escalation Ladder

1. Keep behavior in the current owner module and strengthen tests.
2. Extract a named helper/service inside the same module when one function does multiple domain jobs.
3. Tighten an anti-corruption contract when facts cross into another domain's action surface.
4. Add a compact read model or background projection inside the monolith when repeated expensive computation blocks a first-screen or notification path.
5. Consider fuller CQRS/eventing only after measured pain shows local fixes cannot provide correctness, latency, reproducibility, or reviewability.

## Today-Actions Boundary

Treat `/api/decision/today-actions` as a rider-facing observation read model. Raw decision action, candidate evidence, review pack data, shadow reference, or LLM text is evidence only. `advice_contract` owns executable semantics.

GET/read-model paths must not secretly create durable decisions, orders, trades, positions, or broker actions.

## Workflow

1. Identify the owner module and consumer surface.
2. Map producer -> anti-corruption contract -> read model/consumer.
3. State whether the issue is local, cross-boundary, latency/projection, or architecture-level.
4. Choose the lowest rung on the escalation ladder that can satisfy the proof standard.
5. Add tests that prove blocking behavior or boundary preservation, not just field presence.

## Response Shape

```text
Owner module:
Consumer surface:
Boundary crossed:
Chosen scale rung:
Why heavier architecture is not justified:
Patch target:
Acceptance test:
Residual risk:
```
