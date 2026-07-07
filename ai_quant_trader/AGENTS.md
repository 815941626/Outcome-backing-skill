# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

AI Quant Trader — an AI-powered quantitative trading assistant for Chinese A-stocks, US stocks, and Hong Kong stocks. FastAPI backend + vanilla JS frontend SPA, SQLite (WAL mode), multi-account architecture with JWT auth.

## Core Collaboration Rule: Honest Uncertainty

Codex is an LLM, not an all-knowing authority. It is acceptable and expected to say "I do not know yet", "I am not sure", "I do not understand the target", or "I need to verify this" when the goal, evidence, data definition, code path, market meaning, or available capability is unclear.

When uncertain, do not perform confidence. Instead:
- state what is known from current evidence
- state the unknown, ambiguity, or risk
- propose the smallest verification step or the smallest necessary user question
- continue investigating locally when the uncertainty can be checked from code, data, logs, tests, or docs
- ask the user only when a real product/trading decision cannot be inferred safely

Never invent user intent, evidence, causality, market conclusions, data freshness, source coverage, or implementation details to appear capable. In trading work, missing, stale, or insufficient data must stay visible as missing, stale, or insufficient; it must not be converted into a confident signal.

### Parallel Subagents

Default to a single Codex agent for ordinary implementation, small fixes, routine checks, and sequential debugging. Use built-in parallel subagents proactively only for architecture review, whole-system planning, active-goal/systemic audits, or broad evidence checks where independent code, data, UI, test, deploy, documentation, or market-evidence tracks can reduce blind spots.

If Codex reaches a real uncertainty or blocker in one step (such as not understanding the target, not knowing which code path owns the behavior, or seeing conflicting evidence), it should say so and may launch parallel subagents to investigate bounded hypotheses before proceeding. Parallel agents must not replace uncertainty disclosure, source verification, or the smallest necessary user question. Codex must merge subagent findings into one evidence-backed conclusion, explicitly calling out conflicts, missing data, and residual risk.

## Trading Hot-Path Rule: Alpha Before Bureaucracy

AI Quant Trader is a trading system first. Do not silently redefine success from "make better buy/sell decisions" into "prove the system is harmless." Safety boundaries matter, but the product outcome is improved risk-adjusted action.

For the next three active-goal iterations after 2026-06-29, default P0 is hot-path only:
- improve or evaluate `entry_price`, `entry_anchor`, `stop_loss`, target, planned shares, expected R, missed upside, drawdown, or buy-vs-no-buy outcome
- compare action vs inaction on real or replayed price paths
- make false negatives visible as costly failures, not neutral non-events

During those iterations, do not create new Contract, Audit, Snapshot, Review, Sync, Task, dry-run, or confirmation layers unless the user explicitly asks for that layer or there is an immediate real-account safety or data-loss defect. If a proposed change mainly adds governance, say it is cold-path work and stop.

Four-module development discipline:
- keep the product shape as `market_structure` (big-picture regime), `stock_pool` (ticker attributes, lifecycle, and playbook fit), `observation` (current ticker-state judgment plus durable notes for review), and `review` (post-outcome attribution that feeds corrections back into the first three modules)
- every code change must name the concrete trading problem it solves; "more observability" is not a sufficient reason
- acceptable reasons include reducing costly missed buys, preventing bad buys, cutting avoidable drawdown, clarifying ticker lifecycle/state, or making a past judgment reviewable enough to change future market-structure, stock-pool, or observation rules
- do not build observation-of-observation layers; observation code is useful only when it improves current judgment or records the judgment so review can falsify it later

Required acceptance for a hot-path iteration:
- it changes or evaluates a buy/sell/entry/stop/sizing rule against price data
- it reports expected R, realized or forward R, missed upside, or drawdown
- it preserves outer account risk controls without making inner research/simulation more bureaucratic as the main deliverable

Hard distinction:
- outer safety: account isolation, real-account no-auto-order, max loss, broker/trade truth, and data-loss protection; preserve these
- inner hesitation: expanding `review_only`, `dry_run`, `confirmed_by_user`, or "cannot act" states inside research/simulation; do not expand these as the answer to an alpha problem

## Engineering Scale Rule: Modular Monolith + Anti-Corruption First

The best-fit architecture for this repo is a modular monolith with clear domain boundaries, CQRS-like read/write separation where it already protects hot paths, and explicit anti-corruption layers between raw evidence and rider-facing action semantics. Do not jump to a full CQRS/event-sourced/microservice rewrite unless measured evidence shows the monolith cannot provide correctness, latency, reproducibility, or reviewability.

Do not confuse "smallest useful change" with "shortest patch." The right default is the smallest durable change that preserves the trading hot path and keeps future refactors cheaper. A direct patch is acceptable only when it does not create a new cross-module dependency, bypass an action contract, hide stale/missing evidence, or make a future review unable to falsify the decision.

Planning scale by change type:
- Local bug or display issue: make a focused patch, but still name the trading or safety result it protects and add/adjust the narrow test that proves it.
- Cross-boundary change touching `today-actions`, action permission, order planning, shadow auto-exec, or review-derived evidence: first map producer -> anti-corruption contract -> read model/consumer, then patch the boundary rather than copying raw fields across modules.
- Hot-path latency or repeat computation issue: prefer request-context reuse, compact read models, cache/projection inside the monolith, or background precomputation before proposing a new architecture family.
- Architecture proposal: compare current code shape, modular-monolith target, and heavier alternatives. Reject fashionable patterns when they do not improve action quality, latency, auditability, or future change cost.
- Broad/systemic uncertainty: use bounded parallel subagents or a short outcome tree to inspect independent code/data/UI/test paths, then merge evidence into one concrete plan.

Architecture escalation ladder:
1. Keep behavior in the current owner module and strengthen tests.
2. Extract a named helper/service inside the same module when a function is doing multiple domain jobs.
3. Add or tighten an anti-corruption contract when facts cross from one domain into another domain's action surface.
4. Add a compact read model or background projection inside the monolith when the same expensive computation must serve a first-screen or notification path repeatedly.
5. Consider fuller CQRS/eventing only after there is measured pain: inconsistent read/write truth, unrepeatable decisions, cold-path latency that cannot be fixed locally, or multiple consumers requiring stable historical snapshots.

## Today Actions Anti-Corruption Boundary

`/api/decision/today-actions` is the rider-facing observation read model. It may summarize decisions, holdings, prices, risk, candidate evidence, static anchors, managed plans, and review-only context, but it must not let those raw inputs become trade permission by implication.

Rules for this boundary:
- Raw `decision.action`, `buy_candidate_evidence`, `decision_brief_review`, `shadow_reference`, review pack data, or LLM text is evidence only. None of them is a buy/sell permission by itself.
- `advice_contract` owns executable semantics such as `is_executable`, `manual_order_recommended`, `bucket`, `status_reason`, `plan_complete`, and freshness/block reasons.
- `execution_view` and `managed_trade_plan` may explain or package the contract result, but they must not weaken it or recreate permission from raw fields.
- GET/read-model paths should not secretly create durable decisions, orders, trades, positions, or broker actions. If a write is needed, it must be an explicit POST/command path with a post-write readback check.
- Review-only or diagnostic payloads must remain opt-in, compacted away from the first-screen read model unless the user explicitly asks for diagnostics.
- Any new consumer of Today Actions must consume the contract fields first. If it needs a raw field, the change must say why the contract is insufficient and whether the contract should be extended instead.
- Tests for this area should prove blocking behavior, not only presence of fields: stale price, stale decision, missing plan, account mismatch, review-only candidate, market no-new-open, and risk guard should fail closed while sell/exit paths remain available when appropriate.

Domain ownership remains:
- `market_structure`: regime and opportunity environment facts.
- `stock_pool`: ticker attributes, lifecycle, playbook fit, and recurring failure modes.
- `observation`: current ticker-state judgment, Today Actions, action contract translation, and durable notes needed for review.
- `review`: post-outcome attribution that feeds corrections back into market structure, stock pool, and observation rules without directly granting current trade permission.

## Commands

### Start the server
```bash
cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Frontend is served as static files by FastAPI from `frontend/` at root `/`. No separate frontend build step.

### Run tests
```bash
cd backend && pytest              # all tests (~365 as of 2026-04-18, runs <30s)
cd backend && pytest -v           # verbose
cd backend && pytest -k test_race_plan   # by pattern
cd backend && pytest tests/test_engine.py  # single file
cd backend && pytest --cov        # with coverage
```

### Install dependencies
```bash
pip3 install -r backend/requirements.txt
```

## Architecture

### Decision Pipeline (core intelligence)
```
Price Data (OHLCV from Sina/Eastmoney/YFinance)
  → Technical Signals (RSI, MACD, MA, Volume, ATR) in strategy/signal_generator.py
  → News Signals (sentiment, time-decay weighted) in news/
  → Situation Detection (context-aware refinement) in strategy/situations/
  → Weighted Score → Action (buy/sell/hold/add/reduce) in decision/engine.py
  → Position Advisor (7-level exit checks) in decision/position_advisor.py
  → RacePlan auto-generation in decision/race_plan_manager.py

For shadow accounts with auto-execute enabled, the decision output also flows:
  → auto_exec_policy (layered kill-switch check)
  → trade_gate (5 safety rules: hours, daily-loss, max-adds, risk, cash)
  → execute_auto_trade → tracker (or paper mode, no-op)
```

### Backend Structure
- **main.py** — FastAPI app, CORS config, legacy endpoints (~60 routes total)
- **database.py** — SQLite schema, migrations, WAL mode. All tables use `account_id` for multi-account isolation. Triggers prevent `account_type='real'` rows from ever having `auto_execute=1`
- **auth.py / auth_router.py** — JWT (HS256, 7-day expiry), SHA-256+salt passwords. `get_account_id_dep()` is the auth dependency used by most endpoints. Self-registration NOT exposed (SQL-only)
- **decision/** — Engine orchestration, position exit logic, race plan management. Shadow-as-account adds:
  - `auto_exec_policy.py` — `assert_auto_exec_allowed(account_id)` (real account blocked, kill-switch, type/mode/flag checks)
  - `trade_gate.py` — 5 pre-trade circuit breakers; every attempt (pass or block) logs to `trade_gate_log`
  - `auto_execute.py` — `execute_auto_trade(account_id, decision, price_data)` composes policy → gate → tracker/paper
  - `auto_cycle.py` — iterates eligible shadow accounts, drives the full cycle
- **strategy/** — Rule engine, signal generators, plan generators. All thresholds parameterized via `support_team/quantlib/` param registry. Per-account overrides flow through `param_registry.use_overrides(...)` scoped context (thread-local)
- **news/** — Crawlers (Sina, YFinance), sentiment analysis, aggregation
- **performance/** — Trade recording, PnL tracking, position management (tracker.py)
- **alarm/** — 警铃: daily health sentinels (D1 OHLCV / B1 decision count / B2 direction collapse / X1 shadow 0-sell / P1 archive produced / S1 error log count). `run_daily_check(date)` fires at 15:30 CST via scheduler, writes `daily_health_check` + `data/health/daily_YYYYMMDD.md`. API: `/api/health/{run,today,history}`
- **trainer/** — FROZEN (see `trainer/__init__.py`). Kept for future monitor-UI repurpose. `SimPortfolioManager.sim_buy/sim_sell` still used by `execute_auto_trade` as the shadow-account write path; `SimTrainer` class no longer driven by scheduler
- **scheduler.py** — Background news crawling, intraday decision cycles, daily archive (15:15), daily health sentinel (15:30), shadow auto-execute cycle
- **core/config.py** — Settings loaded from `.env`. `AUTO_EXEC_GLOBAL_ENABLED=true` required to unlock any shadow auto-trading
- **core/error_log.py** — `setup_error_logging()` attaches ERROR-level FileHandler to `data/logs/errors.log` for S1 sentinel

### Frontend Structure
- **app.js** — `apiFetch()` wrapper (adds Bearer token + X-Account-Id header), Auth module, AppState, tab routing
- **tabs/overview.js** — Portfolio dashboard with watchlist management (6-digit A-share code validation)
- **tabs/decision.js** — Decision center UI
- **tabs/news.js, performance.js, plans.js, system.js, shadow.js** — Other tab modules
- API_BASE: `http://localhost:8000/api` for local dev, `${window.location.origin}/api` for production

### Multi-Account Model
- `users` table → `trading_accounts` table (1:N). Default user "骑手" (id=1) owns real account (id=1) + shadow accounts (id=2,3)
- Every DB table with positions/trades/decisions/race_plans has `account_id` column (default=1)
- `get_account_id_dep()` extracts account from JWT + X-Account-Id header, validates ownership
- `trading_accounts` carries 4 extra columns for shadow behavior: `auto_execute`, `execution_mode` (advisory/paper/auto), `param_overrides_json` (per-account strategy tuning), `gate_config_json` (per-account safety rules)
- Three-layer kill switch for shadow auto-exec: `.env AUTO_EXEC_GLOBAL_ENABLED` + `account.auto_execute=1` + `account.execution_mode in {paper,auto}`. Any layer off → no auto-trading. DB trigger physically prevents real accounts from enabling any layer

### Database
SQLite with WAL mode at `backend/data/quant_trader.db`. Schema managed in `database.py` with incremental migrations. Key constraints: `UNIQUE(account_id, ticker)` on positions and race_plans.

## Key Patterns

### Dependency Injection
```python
# Pluggable providers configured in main.py
def get_data_provider():   # returns SinaNewsProvider or YFinanceProvider
def get_ai_engine():       # returns OpenAIEngine or FinBERTEngine
_get_account_id = get_account_id_dep()  # JWT auth + account validation
```

### DB Access
```python
from database import get_db
with get_db() as conn:
    rows = conn.execute("SELECT ... WHERE account_id = ?", (account_id,)).fetchall()
# Auto-commit on exit, auto-rollback on exception
```

### Test Fixtures
Tests use in-memory SQLite with full schema (see `tests/conftest.py`). No external services needed.

## Documentation

- **DECISIONS.md** — Chronological architecture decision log in trader-friendly Chinese. Newest entries first. Update after significant changes (triggered by "帮我翻译一下")
- **STRATEGY.md** — Trading philosophy: 后勤组(strategy layer) → 马(execution layer) → 骑手(decision layer). Rule priority system (核心/辅助/参考)
- **ROADMAP.md** — Priorities and tech debt tracking
