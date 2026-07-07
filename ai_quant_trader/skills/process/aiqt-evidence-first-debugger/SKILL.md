---
name: aiqt-evidence-first-debugger
description: Use for AI Quant Trader debugging when the user challenges truthfulness, says the agent is lying, says no code/log/data was checked, asks why live behavior differs from the explanation, reports cloud/local mismatch, today-actions error/timeout, missing buy/sell/order, or any incident where Codex must prove the current code/data/log chain before explaining causality.
---

# AIQT Evidence-First Debugger

## Purpose

Prevent confident false explanations in AI Quant Trader work. Treat every incident as unverified until current code, data, logs, or live service evidence supports it.

Use this skill to answer: what is actually known, what is still unknown, and what smallest check proves or falsifies the explanation?

## Core Rule

Do not explain from memory or architecture diagrams when the user reports a live or ticker-level failure. Inspect the current path first.

Acceptable evidence grades:

- `data_verified`: current code/data/log/live command proves the statement.
- `structurally_plausible`: current code shape supports the hypothesis, but live data is missing.
- `memory_derived`: prior memory suggests it, but it may be stale.
- `narrative_only`: no current evidence; do not present as a conclusion.
- `contradicted`: current evidence disproves the claim.

## Workflow

1. Restate the observed symptom and the desired normal result.
2. List the minimum evidence needed before explaining cause.
3. Inspect current repo code before naming a code-path cause.
4. Inspect current DB/log/live service before naming a production cause.
5. Separate facts from hypotheses in the response.
6. If the first explanation fails, update the evidence ledger instead of defending it.
7. If data is missing or stale, keep it visible as missing or stale.

## Required Output

Use this compact shape:

```text
Observed symptom:
Normal result expected:
Evidence checked:
- code:
- data/log/live:
Verified cause:
Hypotheses still open:
Smallest fix or next check:
Proof that it worked:
```

## AIQT Guardrails

- For ticker complaints, inspect ticker-specific rows or payloads when available.
- For today-actions issues, check frontend timeout, backend route, cache behavior, live status code, and service logs before proposing architecture work.
- For trade/buy/sell issues, trace from notification or UI surface to `advice_contract`, managed plan, preflight/formal authority, and trade ledger.
- For cloud incidents, measure live service behavior before assuming the latest local code is deployed.
- Never convert a ServerChan alert, review-only field, LLM text, or raw decision action into executable permission without checking the contract boundary.
