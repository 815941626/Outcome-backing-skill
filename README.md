# Agent Logic Center

This repository is the source of truth for reusable agent logic, project constraints, and Codex skills.

It is not only the outcome-backward skill. It also stores domain-specific agent rules that can be synced to new machines.

## Layout

- `SKILL.md`: the core outcome-backward skill.
- `outcome-tree/`: validators and renderers used by the outcome-backward skill.
- `ai_quant_trader/`: AI Quant Trader agent constraints and skills.

## Current Domain Packs

- `ai_quant_trader/`: quantitative trading assistant for Chinese A-shares, US stocks, and Hong Kong stocks. Contains project-level `AGENTS.md`, AIQT role skills, and process skills learned from production incidents.
