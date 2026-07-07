# AI Quant Trader Agent Logic

This folder stores agent rules for the `ai_quant_trader` project.

## Purpose

AI Quant Trader is a trading system first. The agent rules here preserve the lessons learned from real project failures:

- say uncertainty instead of inventing evidence
- inspect current code, data, logs, and live service state before explaining failures
- keep P0 work on the hot trading path when the problem is buy/sell/entry/stop/sizing quality
- avoid cold bureaucracy such as extra audit/snapshot/review layers unless they solve a real trading, safety, or data-loss problem
- keep the architecture at modular-monolith scale with clear anti-corruption boundaries

## Files

- `AGENTS.md`: project-level constraints to copy into the root of an `ai_quant_trader` checkout.
- `skills/strategy/`: regime, playbook, and evaluator skills.
- `skills/research/`: quantitative evidence and parameter skills.
- `skills/risk/`: truth, safety, account-scope, and execution-boundary skills.
- `skills/review/`: closed-loop review and post-market attribution skills.
- `skills/collaboration/`: roundtable and multi-role discussion skills.
- `skills/process/`: process guardrail skills created from recurring AIQT failure modes.

## Recommended Install On A New Machine

From this repository root:

```bash
bash ai_quant_trader/install.sh /path/to/ai_quant_trader
```

The script copies `ai_quant_trader/AGENTS.md` into the target project root and installs every AIQT skill into `${CODEX_HOME:-$HOME/.codex}/skills/`.

## Skill Count

Current AIQT skill set:

- 8 existing role skills copied from the live Codex skill directory
- 3 process guardrail skills created from recurring AIQT workflow failures

Total: 11 AIQT skills.

Do not create more skills just because a topic exists. Add a new skill only when the behavior recurs across tasks and cannot be reliably enforced by `AGENTS.md` alone.
