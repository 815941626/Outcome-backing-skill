---
name: aiqt-roundtable-meeting
description: "Use for AI Quant Trader roundtable meetings and structured multi-role debates. Trigger when the user asks 开会, 圆桌会议, 线性讨论, 后勤组会议, 让几个角色讨论, or wants Codex to chair strategist/evaluator/analyst/quant/risk roles around one outcome-led dispute and produce a decision plus next action."
---

# AIQT Roundtable Meeting

## Role

Act as the meeting chair, not another panelist. The user is the owner/boss who sets the target; Codex chairs the meeting, asks narrow questions, controls speaking order, forces each role to respond to the previous role, and converts the discussion into a decision and next action.

This skill exists to avoid five independent reports. A valid meeting must have a shared dispute, linear turns, cross-response, and a final decision.

## When To Use Subagents

Use subagents only when the user explicitly asks to派 agent/subagent, 让几个角色开会, 并行角色讨论, or otherwise clearly delegates work to agents.

If the user only says "用开会方式想一下" without explicit subagents, simulate the roles locally in the main thread.

## Default AIQT Roles

Default roundtable members:

- Strategist: `$aiqt-strategist`
- Model evaluator / 军师: `$aiqt-model-evaluator`
- Post-race analyst: `$aiqt-postrace-analyst`
- Quant researcher: `$aiqt-quant-researcher`
- Risk auditor: `$aiqt-risk-auditor`

Use these default roles for AI Quant Trader unless the user names a different set.

## Meeting Protocol

### 1. Set The Dispute

Start with one concrete dispute, not a broad request.

Good examples:

- "现在最该先补数据，还是先改买入逻辑？"
- "突破买入应该进入正式策略，还是只留在反事实复盘？"
- "5 月目标最大的瓶颈是机会发现、买入转化、风控，还是闭环样本？"

Bad examples:

- "大家怎么看系统？"
- "各自给一份方案。"

### 2. Roll Call Only

If using subagents, first start or resume the roles and ask only for one-line readiness. Do not let them submit reports during roll call.

### 3. Round 1: Diagnose The Dispute

Chair asks one role to begin. Each next role must respond to the previous role and take a side.

Use prompts like:

```text
总经理点名：只回答这个争议，不写完整方案。你必须回应上一位。
你的判断是 A 还是 B？为什么？
限制 400-500 字。
```

Chair summarizes the round in one paragraph before moving on.

### 4. Round 2: Define The Capability

Turn the diagnosis into one capability.

Use prompts like:

```text
总经理第二轮点名：基于上一轮结论，定义这个能力应该长什么样。
哪些输入必须进？哪些字段必须固定？哪些只能 review-only？
限制 500 字。
```

Every speaker must build on or challenge the previous speaker. Do not allow role-isolated reports.

### 5. Round 3: Chair Proposal And Vote

Chair proposes one concrete decision with P0/P1/P2 shape. Each role may only answer:

```text
同意/反对 + 一个修改条件。
```

If any role rejects the proposal, chair must revise the proposal once and re-vote.

### 6. Close The Meeting

Final answer should include:

- Meeting dispute.
- Linear discussion summary.
- Decision.
- What to do next.
- What explicitly not to do.
- Any follow-up implementation plan if the user asked to proceed.

## Chair Rules

- Keep the meeting result-led. Use outcome-backward logic when the topic involves goals, ROI, revenue, safety, or strategy.
- Prevent report mode. If a role starts listing everything, interrupt or constrain the next prompt.
- Ask narrow questions and enforce word limits.
- Force disagreement to be explicit.
- Force every non-trivial claim through the support-team judgment contract:
  result, falsifiable assumption, evidence grade, tradeoff, and smallest closed-loop action.
- Ask each next speaker to challenge either the previous speaker's assumption, evidence grade, cost, or proposed next action.
- Preserve hard boundaries: no auto real trading, no stale data execution, no stop no trade, API is candidate/explanation unless explicitly promoted by rules.
- Close with an actionable decision, not a summary of opinions.

## AIQT Meeting Template

For the common AIQT support-team meeting:

1. Dispute: "现在最该先补数据，还是先改买入逻辑？"
2. Round 1:
   - Strategist: identify strategic bottleneck.
   - Post-race analyst: challenge with evidence and data gaps.
   - Quant researcher: define minimum sample needed.
   - Risk auditor: state what can change without endangering capital.
   - Model evaluator: make the priority verdict.
3. Round 2:
   - Post-race analyst: define evidence universe.
   - Strategist: define strategic permission.
   - Quant researcher: define metrics and replay fields.
   - Risk auditor: define execution boundaries.
   - Model evaluator: name the capability.
4. Round 3:
   - Chair proposes P0/P1/P2.
   - All roles vote with one condition.
   - Any accepted P0 must name owner role, verification window, and downgrade condition if wrong.

## Output Tone

Write the final meeting result in Chinese for this repo unless the user asks otherwise. Keep it concise enough to act on.
