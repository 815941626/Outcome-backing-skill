---
name: outcome-backward-working
description: Use when Codex handles non-trivial planning, implementation, debugging, review, product, business, architecture, strategy, ROI, revenue goals, success criteria, roadmaps, "结果倒推", "目标反推", "can this achieve X", or "what should we build/fix next". This skill makes Codex work backward recursively from the desired result, score the distance to goal, create prioritized subtasks from the weakest capabilities, reuse existing system capabilities first, delegate specialist thinking only when appropriate, then converge on implementation and verification.
---

# Outcome Backward Working

Use this skill to make work result-led, recursive, and evidence-bound. Do not merely ask "what file should change?" First ask what result must become true, what would prove it, and what capabilities must exist for that proof to be possible.

The core pattern is:

```text
Outcome -> proof standard -> required capability -> existing support -> gap
        -> distance score -> prioritized subtasks -> branch hypotheses
        -> test/compare -> converge -> implement -> verify -> rescore
```

## Fast Operating Protocol

When this skill triggers, first choose the smallest mode that can honestly
protect the outcome:

```text
Compact mode:
  Use for small, local, or mechanical requests.
  Output one result sentence, one proof/acceptance check, then execute.

Focused mode:
  Use for normal analysis, design, debugging, or feature work.
  Output root outcome, domain ruler, direct child needs, weakest gap,
  chosen next action, and verification.

Full tree mode:
  Use for strategic, ambiguous, high-impact, long-running, money/safety, or
  user-requested outcome-tree work.
  Build or update the visible outcome tree and score capabilities.
```

Do not dump the full template when Compact or Focused mode is enough. Do not
hide the reasoning when Full tree mode is needed. The mode choice should be
based on outcome risk, ambiguity, and reversibility, not on answer length.

For most user-facing replies, use this stable process shape:

```text
Mode:
Root framing:
Problem frame when diagnosing:
Root outcome:
Domain / specialist lens:
Domain ruler:
Recursive depth target:
Direct child results the parent needs:
Expanded recursive chains:
Weakest current gap:
Next action:
Proof / verification:
Residual risk:
```

For practical everyday requests such as recipes, crafts, learning plans, or
small workflows, do not force those labels if they would make the answer stiff.
Instead, the public answer must still show a compact causal chain in natural
language:

```text
To get <target result>, we need <child condition>; therefore choose <action>.
If <child condition> is absent, <failure mode> happens.
```

A good answer should include:

- the target result in the user's words,
- 3-5 key choices with plain "why this choice works" explanations,
- the concrete plan or recipe,
- the proof/acceptance check,
- the first adjustment loop if the result is weak.

Do not leave the outcome tree only inside hidden reasoning. The user should be
able to see why the chosen plan follows from the target result, without needing
to read a formal tree.

### Problem Discovery / Analysis / Solution Overlay

When the user asks why something failed, whether a judgment was wrong, what is
wrong with a system, how to fix a recurring weakness, or asks for diagnosis,
embed this three-step problem loop before choosing the final answer:

```text
1. Discover the problem:
   Separate the observed symptom from the desired normal result.
   Ask what result should have been true, what actually happened, where the
   gap appeared, and what evidence is already visible.

2. Analyze the problem:
   Treat the missing normal result as the parent outcome.
   Derive direct child results it needed, then mark which child is absent,
   weak, unproven, or only a hypothesis.

3. Solve the problem:
   Convert the weakest validated gap into an action, boundary, or repair loop.
   State what would prove the fix worked and what would invalidate it.
```

This overlay does not replace outcome-backward reasoning. It is the entry gate
for problem-shaped requests:

```text
Observed symptom -> desired normal result -> missing required child result
                 -> evidence / hypothesis split -> repair action
                 -> verification / invalidation
```

For visible answers, keep the distinction clear:

```text
Observed problem:
Normal result that should become true:
Likely missing child result:
Evidence that supports this:
What is still only a hypothesis:
Action / repair:
Proof that the repair worked:
```

Do not solve from the symptom directly. For example, "the stock fell after I
bought" is a symptom. The local parent result may be "the entry has enough
right-side confirmation and a known invalidation point." The analysis should
then ask which required child result was missing: sector support, price
acceptance, volume follow-through, risk boundary, or execution discipline.

If the problem is ambiguous, produce competing cause hypotheses, but each
hypothesis must still attach to a missing child result in the outcome tree. Do
not leave hypotheses as loose commentary.

This skill builds a tree of mechanisms and conditions for an outcome to become
true. It may use fields, components, modules, or page sections as clues, but it
must not stop at them.

### Recursive Depth Contract

Outcome-backward work is recursive by default. Do not stop after one layer of
direct child results unless the request is truly compact or every child is
already a proof-ready leaf.

Count depth by visible result nodes, not by edges:

```text
Layer 1: root outcome
Layer 2: direct child results the root needs
Layer 3: direct child results each Layer 2 node needs
Layer 4+: use a separate rerun with a Layer 2 or Layer 3 child as the new root
```

Default depth:

```text
Compact mode: 2 visible layers, plus one proof/acceptance check.
Focused mode: 3 visible layers for the current root result.
Full tree mode: 3 visible layers for the current root result, then rerun on
  one child result if deeper recursion is needed.
```

If the user names a depth, such as "推 9 层", that requested depth overrides the
default, but keep the process readable. Build the 3-layer tree for the current
root first. For deeper recursion, rerun the skill with the chosen child result
as the new root, or explicitly re-root on the weakest/highest-risk child if the
next step is obvious. Do not explode one giant tree.

Every accepted child that is not a leaf must be re-entered as a new parent:

```text
Parent: <child result from the previous layer>
Ask again: for this parent result to become true, what direct child results
must already be true?
```

A node is a leaf only when it is directly actionable, has a clear proof check,
and splitting it further would not change the next action or verification. If
you stop before the target depth, label the node as a leaf and state why.

For visible output, prefer a compact recursive table or outline:

```text
Path / layer:
Parent result:
Child result:
Why parent needs child:
What fails if absent:
Proof or action:
```

### Width And Node Budget Contract

Do not make a parent look understood by giving only one or two causes. For the
current root run, every expanded non-leaf parent should have 5 direct child
results by default.

Default budget:

```text
Depth target: 3 visible layers.
Minimum children per expanded parent: 5.
Maximum children per expanded parent: 5, unless the user asks for wider.
No hard total-node cap. Use the smallest readable tree that covers the result.
```

If fully expanding every layer-2 branch would make the answer too long for the
user's requested format, expand the weakest, highest-risk, or most
decision-relevant layer-2 parents first. Mark the remaining layer-2 siblings as
`deferred-for-rerun` leaves and give a rerun prompt such as:

```text
Rerun outcome-backward-working with this as the root outcome:
<deferred child result>
```

If a genuinely narrow parent has fewer than 5 real causes, do not invent fake
children. Add explicit unresolved slots instead, with the visible child result
`想不出来 / unresolved cause slot`, and say what domain input would be needed to
fill it. Unresolved slots preserve the coverage gap; they do not count as
validated causal knowledge.

### Root Framing Gate

Before building the recursive tree, pass the root through a visible or internal
root-framing check. Outcome-backward work is only valid after the chosen root is
the user's real target result, not a symptom, tool, intermediate action, or old
context leak.

For every non-trivial run, establish:

```text
Raw user ask:
Selected root outcome:
Why this root is the real target:
Domain fit:
Why the proof standard matches the root:
Boundary / non-goals:
Misread risk:
Clarification needed:
```

The root is admitted only if:

```text
The selected root outcome preserves the user's concrete target.
The root is observable in the relevant domain.
The proof standard would actually prove that root, not just prove a subtask.
Known history, old trees, examples, and remembered modules did not choose the
root; they may only supply evidence or boundaries after the root is admitted.
If two or more plausible roots would change the answer materially, ask a narrow
clarifying question before building the tree.
```

If the user asks to see the process, the public answer should show this root
framing before the recursive parent-child table.

### Structured Process Gate

Plain text instructions are not enough when the user needs to audit whether the
assistant actually followed outcome-backward logic. For non-trivial, high-risk,
money/safety, user-challenged, or explicitly "show the process" tasks, first
create or internally hold an Outcome Process JSON before writing the final
answer.

Use:

```text
<SKILL_DIR>/outcome-tree/outcome_backward_process.schema.json
<SKILL_DIR>/outcome-tree/validate_outcome_process.py
<SKILL_DIR>/outcome-tree/render_outcome_process_markdown.py
```

The process JSON is the hard shape for the reasoning ledger:

```text
root_framing[raw_user_ask, selected_root_outcome, root_admission,
             domain_fit, proof_standard_reason, boundary, misread_risk,
             clarification_needed, clarification_question]
problem_solving[problem_mode, observed_symptom, desired_normal_result,
                problem_statement, evidence_seen, likely_missing_child_result,
                hypothesis_vs_evidence, repair_strategy, verification_check]
root_outcome
domain + domain_ruler
depth_target
width_policy[min_children_per_parent, max_children_per_parent, max_total_nodes]
nodes[id, layer, result, parent_id, is_leaf, proof_check]
edges[parent_id, child_id, parent_needs_child, failure_if_absent, child_admission, proof_or_action]
next_action
residual_risk
```

Do not treat a prose outline as sufficient when this gate applies. The visible
answer may summarize the JSON, but it must preserve the same parent-child edges
and the same depth target. If a draft answer cannot be represented in this JSON
shape, the draft has not followed the skill.

When the user asks to see the process, every layer, or the full recursive
result chain, the public answer must be a projection of the JSON edge list, not
a newly hand-shaped outline. Use the same columns for every layer:

```text
Path
Layer
Parent result
Child result
Why parent needs child
What fails if absent
Proof / action
```

Do not weaken the structure as layers get deeper. Do not switch L2 to a
different table shape from L3 or L4. Leaf/action rows still need their parent,
why-needed, failure, and proof/action edge text. Prefer running
`render_outcome_process_markdown.py <process.json> --strict` and using that
output as the visible process table, then add only a short plain-language
summary if needed.

Validation rules:

```text
Root framing exists before the tree.
root_framing.raw_user_ask matches user_request.
root_framing.selected_root_outcome matches root_outcome.
Root admission says why the root is the user's true target, not a symptom/tool.
Boundary and misread risk are explicit before child derivation starts.
For problem-shaped requests, problem_solving exists and separates symptom,
desired normal result, missing child result, evidence, hypothesis, repair, and
verification.
One root at layer 1.
Every non-root node has exactly one parent edge.
Every edge increases layer by one.
Every edge states why the parent needs the child and what fails if absent.
Every non-leaf before depth_target must recurse.
Every expanded non-leaf parent should have at least 5 child slots by default.
If max_total_nodes is set, treat it as a readability budget, not a fixed
skill-wide cap.
Every early leaf must say why it is proof-ready / directly actionable.
Deferred early leaves must say they are deferred-for-rerun and include the
child result to use as the next root.
```

### Child Admission Test

This is the hard gate for every tree edge:

```text
Parent result requires child result.
Without this child result, the parent becomes false, unproven, unsafe,
unreviewable, or materially incomplete.
```

A proposed child is allowed into the tree only when the assistant can write
that parent-needs-child sentence plainly. If the sentence is weak, the item is
not a child at this layer. Move it to target shape, existing support,
implementation option, deferred risk, or a lower-level node.

Before accepting a child, test:

```text
Is this a direct condition for the current parent result?
What breaks in the parent if this child is absent?
Is the child a mechanism/result, not just a field, module, label, or topic?
What proof would show this child is actually true?
```

If these questions cannot be answered, do not keep the child. Re-derive from
the current parent result instead of filling the tree with related ideas.

### Literal Text Is an Entry, Mechanism Is the Cause

字面是入口，不是原因；拆解是探针，不是证据；机制才是因.

An outcome can have fields, slots, sections, object properties, modules, or
surface wording. These are useful entry points for thinking, but they are not
automatically the direct causes that make the outcome true.

Field or component listing asks:

```text
What parts does this thing contain?
What fields would describe this output?
What modules already exist around it?
```

Use those answers as probes:

```text
This field exists in the target shape. What mechanism makes it true?
This section exists on the page. What condition makes it valid?
This module exists in the repo. What parent result does it actually support?
```

Outcome-backward reasoning asks:

```text
For this current parent result to become true, what direct content factors,
capabilities, evidence, or boundaries must already be true?
```

Fields belong first in `Target shape`, `Domain-valid output`, or an explicit
contract node. Then they can be used as probes to discover the mechanism behind
them. Promote a field-like item into a child only when you can state the
mechanism or condition that makes the current parent depend on it.

Before turning a field-like item into a child, ask:

```text
What mechanism behind this field makes the current parent true?
If this is only a slot, what deeper condition would make the slot valid?
```

If you can only name the slot, keep it inside the contract or target shape. If
you can name the mechanism the parent depends on, make that mechanism a child
and write the parent-needs-child proof.

Example:

```text
Parent: 完整金融有效建议
Field-listing children: 标的, 动作, 价格计划, 为什么, 把握, 错后, 证据, 边界

Outcome-backward children may instead be:
  价格级行动计划
  这笔计划值得做
  判断错了有补救策略
  证据和边界可追溯

Then:
  价格级行动计划
    -> 当前动作判断成立
    -> 入场/触发/最高追
    -> 止损/失效/目标
    -> 放弃条件
```

## Visual Outcome Tree

For a large, strategic, ambiguous, or long-running task, the first pass should
produce a visible outcome tree before implementation. This is the temporary
working table that keeps the assistant from losing the root goal while
recursing into data sources, code paths, and subtasks.

Use this visual pass when the user asks for a big goal analysis, capability
tree, outcome graph, architecture tree, "结果倒推", "目标反推", "从结果往前推",
or when a task can drift into a broad backlog.

The tree shape is:

```text
Root outcome
  -> domain ruler / domain-valid result
    -> user-visible acceptance surface when applicable
      -> product/API contract or workflow
        -> judgment capabilities
          -> data / evidence / feedback
      -> existing support
      -> missing proof / gap
      -> risk / boundary
      -> next P0-P3 subtask
```

Every important node should answer:

```text
Title:
Status: target | ruler | exists | partial | weak | missing | risk | done
WorkStatus: active | done | next | pending | blocked | deferred
Score:
Priority: P0 | P1 | P2 | P3
Local result:
Domain ruler:
Domain-valid output:
Target shape / simulated result:
Parent needs this because:
Need type: output | contract | capability | process | data | evidence | safety | feedback | ops | UX
Need proof:
Proof gate:
Existing support:
Gaps:
Risks / boundaries:
Next subtask:
Owner lens:
```

If a node still reads like a slogan, recurse one level deeper. Stop when the
next node maps cleanly to a data contract, workflow, code path, test,
decision, or evidence source.

### Domain Ruler First

Before decomposing any non-trivial outcome, identify the domain and define the
domain-level meaning of the result. Do this before product surfaces,
architecture objects, schemas, models, data sources, or implementation plans.

This rule exists to prevent a business result from being replaced by a product
shell: 不要把业务果想偏成产品壳. Do not turn "effective advice", "good result", "success", "safe",
"accurate", "profitable", "useful", "reasonable", or similar target words into
only a page, card, API object, field contract, dashboard, or workflow.

For every outcome with a domain-specific quality word, first answer:

```text
Domain:
Domain ruler:
Who judges it:
Minimum domain-valid output:
What would make it wrong or harmful in this domain:
Domain evidence needed:
```

Then make the target shape reflect the domain-valid output, not only the
product container that will display it.

Examples:

```text
Finance target: 总览页有有效建议
Domain ruler: 金融上可行动、可放弃、可复盘、能解释风险和把握的判断。
Minimum domain-valid output:
  <ticker>；<buy/sell/wait/avoid>；<entry_or_trigger>；
  <max_entry_or_not_applicable>；<stop_or_invalidation>；<target_or_exit>；
  <why_buy_or_sell>；<evidence>；<probability_or_sample_insufficient>；
  <if_wrong_repair_action>。

Product shell, not the domain result:
  总览页有一张 card
  brief 被压缩成一句话
  页面有一个字段合同
```

```text
Sports target: 给出有效赛前建议
Domain ruler: 能支持比赛胜负/盘口/阵容/体能/赛程风险判断的建议。
Minimum domain-valid output:
  <match>；<pick_or_no_bet>；<line_or_condition>；<why>；
  <injury_or_rotation_risk>；<confidence_or_sample_limit>；<what_invalidates_it>。
```

If the assistant cannot define the domain ruler, it must inspect domain docs,
current product examples, code, data contracts, or ask a narrow question before
building the tree. A generic UX or architecture decomposition is not allowed
until the domain ruler exists.

### Relative Domain Knowledge Rule

Outcome-backward work must use the domain knowledge that makes the target
non-generic. The assistant should identify the relevant specialist lens and use
just enough of that domain's mechanics, failure modes, and proof signals to make
the tree real.

Pick one primary specialist lens and, only when it changes the proof standard,
one secondary lens. Avoid long panels of fake experts. The lens must change at
least one of these: domain ruler, child needs, proof gate, failure mode, or next
subtask. If it changes none of them, omit it.

For each non-trivial outcome, record:

```text
Specialist lens:
Domain mechanics that matter:
Common failure modes:
Domain proof signals:
What the assistant is uncertain about:
```

Examples:

```text
Baking: flavor extraction, fat/sugar/flour ratio, hydration, dough temperature,
bake color, texture after cooling, storage stability.

Trading: data freshness, decision quality, entry/exit levels, invalidation,
risk boundary, execution discipline, attribution.

Operations: SLO/SLA, error budget, observability, rollback, capacity,
permissions, incident recovery.
```

Do not overclaim domain expertise. If the needed specialist knowledge is
uncertain, inspect reliable local docs/data when available, use conservative
assumptions, or ask a narrow question before turning that branch into a hard
plan.

After the domain ruler is defined, derive:

```text
Domain-valid result
  -> user-visible acceptance surface
    -> product/API contracts
      -> judgment capabilities
        -> data/evidence
          -> feedback/review
```

The exact tree can vary by task, but the domain-valid result must not be
skipped.

### Node-Local Outcome-Needs Rule

Every node is both:

```text
1. A required sub-result for its parent.
2. A local result for its own children.
```

Do not build the tree by listing related ideas, and do not start from a child
then explain how it might cause or relate to the parent. Build each edge by
starting from the parent result and asking what direct child results are needed
for that parent to be true:

```text
Parent result requires child sub-result
```

Before deriving children, first make the parent result concrete. Write a
`Target shape / simulated result`: a short example of what the result would
look like if it were already achieved. If the assistant does not know what that
result should look like, it must inspect the product/code/domain examples,
search the repo, or ask a narrowly scoped question before deriving children.

The simulated result is not truth and not implementation. It is a temporary
ruler that prevents vague decomposition. For a trading result, label it as a
simulation, not investment advice.

Keep simulations clean. Do not copy a user's temporary example ticker, stock
code, price, win rate, sample size, timestamp, position size, trace id, or
other numeric values into the tree unless the user explicitly says those exact
values are the desired target fixture. Prefer neutral placeholders such as
`<ticker>`, `<entry>`, `<max_entry>`, `<stop>`, `<target>`, `<abandon_if>`,
`<sample_size_or_insufficient>`, `<generated_at>`, `<decision_id>`, and
`<calibrated_probability_or_sample_insufficient>`. The target shape should
describe the output form and semantics, not smuggle in unverified market data,
fake runtime facts, or values from a user's ad hoc example.

Example:

```text
Result: 总览页有有效建议
Target shape: 模拟，不是投资建议：
<ticker> <action_label>；入场/触发 <entry_or_trigger>；最高追 <max_entry>；
止损/失效 <stop_or_invalidation>；目标 <target>；放弃 <abandon_if>；
把握 <calibrated_probability_or_sample_insufficient>；
若错 <first_repair_action>；执行边界 <manual_preflight_required>。
```

### User-Visible Result First Rule

If the parent result is something a user should see, read, decide from, operate,
or otherwise experience, first identify the user-visible acceptance surface:
what must visibly appear, become usable, or become understandable for the
parent to be true in the user's eyes.

Do not let the decomposition skip that acceptance surface and become only
internal architecture, schemas, data, models, review loops, or implementation
objects. Those may be direct children only when the parent result itself
explicitly includes an internal proof, safety, reliability, or review outcome
at the same layer; otherwise attach them under the visible/usable result they
support.

For a user-facing parent, start by asking:

```text
For this result to be true in the user's eyes, what visible/usable acceptance
surface must exist? Are there also non-visible proof/safety outcomes that the
parent explicitly requires at this same layer?
```

Then recurse from the accepted visible/proof/safety child results into
contracts, sources, judgment capabilities, data, safety, and feedback.

Example:

```text
Root: 总览页有有效建议
Target shape: 用户第一屏看到一条总结性建议。

Likely visible child for this specific target:
  总览第一屏出现一条总结性建议

Then this child can need:
  固定展示字段
  单一建议来源
  页面优先展示
  不被旧总览逻辑二次裁判
  无建议时显示不能建议的原因

Usually too early if they are the only first-layer children:
  overview_advice_card schema
  advice-center overview_brief
  价格级动作模型
  闭环复盘样本
```

The technical children may still belong in the tree, but place them where the
parent-needs-child proof is direct. If a node title starts with "页面", "总览",
"用户看到", "第一屏", "按钮", "报告", "消息", "提醒", or another
user-visible surface, run this visible-acceptance check before any technical
decomposition. This is a guardrail against skipping levels, not a rule that
forces exactly one child or a fixed child title.

Only after this shape exists should the assistant ask what direct child results
the parent needs. The child list must explain the target shape. If a child does
not help produce or verify the simulated shape, it is likely related noise.

For every parent node, rerun the outcome-backward question locally:

```text
For this exact parent result to be achieved, what direct child results must
already exist?
```

### Local Parent Only

Each recursion step is local. The current node is the only parent result that
may be decomposed. Its children are the direct causes needed for that current
parent to become true. Once a child is selected, that child becomes the new
parent result for the next recursion step.

Do not use the root, grandparent, ancestor categories, global frameworks, or a
previous layer's buckets as the classifier for lower levels. Ancestors provide
boundary and intent only; they do not decide the next child list.

Wrong:

```text
Root: 总览页有有效建议
  -> 领域果 / 可见验收 / 证明
      -> every lower node is forced back into root's 领域/可见/证明 buckets
```

Right:

```text
Root result
  -> direct child causes for root

Child A now becomes the local parent result
  -> direct child causes for Child A

Child A1 now becomes the local parent result
  -> direct child causes for Child A1
```

Before adding any child, ask:

```text
Am I deriving this from the current parent, or am I smuggling in an ancestor's
classification?
```

If the answer depends mainly on the root or a grandparent, move the child to
the layer where that parent-needs-child proof is direct, or defer it.

### Memory Is Evidence, Not Decomposition Logic

Memory, prior work, old trees, known modules, repository history, user
preferences, and previous architecture can help verify facts or enforce
boundaries, but they must not generate the direct child causes for the current
parent.

Use memory only for:

```text
Evidence: "Does this code path already exist?"
Boundary: "Is there a known safety rule, non-goal, or user preference?"
Vocabulary: "What local name does the repo use for this already-derived need?"
```

Do not use memory for:

```text
Decomposition: "What children should this parent have?"
Classification: "Which old bucket does this node belong to?"
Architecture recall: "What existing module can I attach here because it seems related?"
```

Child derivation must come only from the current parent result, its target
shape, and the parent-needs-child proof. After the direct children are derived,
memory may be used to label existing support, gaps, code paths, tests, or
constraints.

Before accepting a child, ask:

```text
If I forgot the old tree, old architecture, and known module names, would this
child still be required by the current parent result?
```

If not, do not add it as a child at this layer. Record it as existing support,
a possible implementation path, or a later verification item instead.

Then test each child with these checks:

- Domain-ruler: if the parent contains a domain quality word, the tree must
  first define the domain-valid result. Product surfaces, cards, schemas,
  APIs, models, and data are invalid as the main line until they support that
  domain result.
- Local-parent-only: the child is derived from the current parent result, not
  from root-level categories, grandparent intent, a global methodology bucket,
  or "this is generally important for the whole goal."
- Memory-clean: the child is not derived from old trees, remembered modules,
  previous architecture, prior implementation details, or user-history context.
  Those may annotate support/gaps only after the child is already justified by
  the current parent.
- Mechanism-not-field: fields, slots, page sections, modules, and object
  properties may be used as entry probes, but the child must name the mechanism
  or condition that makes the current parent true. Do not stop at a field name
  unless the field itself is the governed contract/result the parent directly
  needs.
- Necessary: if this child is absent, the parent becomes false, incomplete,
  unsafe, unreviewable, or unproven.
- Direct: the parent needs this child at this layer, not a sibling, cousin,
  downstream consumer, implementation detail, or vaguely related topic.
- Visible-acceptance: if the parent is user-facing, the decomposition must
  include the visible/usable acceptance surface before dropping into internals.
  Internal contracts, sources, models, data, tests, and review loops are valid
  only when they are direct requirements of the parent at that same layer, or
  when they sit under the visible/proof/safety result they support.
- Level-correct: the child is not skipping an intermediate contract/capability
  and is not prematurely dropping to implementation detail.
- Testable: the child can eventually map to a data contract, code path,
  workflow, manual boundary, evidence source, or acceptance check.
- Sufficient-enough: the children together are enough for the parent result to
  be plausible, while known residual uncertainty is marked as a gap or deferred
  risk.

If any check fails, rename, move, split, merge, or defer the child before using
the tree for implementation. A node such as "总览最简消息" must first have
children that it directly needs in order to exist, such as its source contract,
field contract, and compression rule. A separate node such as "总览第一屏消费这条
消息" may need display priority and old-path downgrade. Do not attach display
cleanup under the message node just because it is related. A deeper node such
as "字段：动作裁判 verdict" must then be treated as its own result and split
into the direct rules, processing capability, and data it needs.

Use edge labels when the relation could be ambiguous. The label should read
like a short "parent needs child" sentence, for example:

```text
overview_brief needs verdict because the brief cannot tell the overview what
to do without a normalized action judgment.
```

Recurse until the branch reaches bottom evidence: raw data, imported fact,
manual input, code path, test, operating rule, or explicit non-goal. In trading
systems, bottom data often means price/K-line, position/account state, thesis,
news, decision history, execution trace, review sample, or freshness metadata.

Keep `Status` and `WorkStatus` separate. `Status` is the maturity of the
capability relative to the outcome; `WorkStatus` is the current implementation
ledger. A node can be `Status: partial` and `WorkStatus: done` when the current
patch has landed but the broader capability still needs evidence or follow-up.

### Static Web Map

This skill includes a small standalone renderer:

```text
<SKILL_DIR>/outcome-tree/render_outcome_tree.py
```

For strict process validation, use the structured process schema before or
alongside the visual map:

```text
python <SKILL_DIR>/outcome-tree/validate_outcome_process.py <outcome-process.json> --strict
```

Use this when the work must prove real recursive outcome-backward reasoning,
not merely display a plausible tree.

For a first-pass visual map:

1. Create an `outcome-tree.json` with `goal`, `proofGates`, `nodes`, and
   `subtasks`.
2. Run:
   ```bash
   python <SKILL_DIR>/outcome-tree/render_outcome_tree.py <outcome-tree.json> --out <outcome-tree.html>
   ```
3. Give the user the HTML path. The page is static and can be opened directly.

The generated page should behave like a working map, not a text outline:
it must support pan, zoom, fit-to-screen, search, status/priority filtering,
node click-through details, and a small overview/minimap when practical.

Default output locations:

- For repo-specific analysis: write to `<PROJECT_ROOT>/.outcome-backward/<slug>/`.
- For skill/tool development examples: write to
  `<SKILL_DIR>/outcome-tree/examples/`.

The graph is not decoration. It is the active ledger for the next work step.
When implementation starts, choose the highest-priority weak node on the tree,
work that node, verify it, then rescore.

During implementation, update the visual ledger with `workStatus`, `workNote`,
and optionally `completedAt` / `evidence` so the map shows what is being fixed,
what has been fixed, and what is next. Do this before moving to another major
node.

## Completeness Audit

The first tree is not enough. After drawing the outcome-needs tree, run a
second-pass coverage audit before choosing implementation work. This is the main defense
against "the tree looks plausible but missed an important branch."

Use this four-pass workflow:

```text
Pass 1: Node-local outcome-needs derivation
  For each important parent, restate it as the local result and derive only
  the direct child results needed for that parent to be true.

Pass 2: Outcome-needs tree
  Outcome needs user-facing output; output needs system contract; contract
  needs capabilities; capabilities need data/evidence.

Pass 3: Coverage audit
  Apply fixed lenses to find missing nodes, hidden assumptions, unsafe shortcuts,
  and unproven proof gates.

Pass 4: Tree repair
  Add or move nodes so every discovered gap is attached to the correct parent.
  Do not leave audit findings as loose notes.
```

The required coverage lenses are:

```text
1. Consumer / user journey:
   Who consumes the output, at what moment, and what must they decide next?

2. Contract / schema:
   What object, API, document, UI surface, or state transition must become the
   ruler? Are fields mandatory, optional, derived, frozen, or display-only?

3. Outcome-needs chain:
   Does the parent result directly need this child result, or is the child
   merely related? If the parent does not need it at this layer, move it to
   the correct branch.
   Re-derive suspicious children from the parent-result question: "for this
   parent to be true, what direct child results are required?"

4. Data lineage:
   Where does each required fact come from? What is fresh, stale, cached,
   inferred, manually entered, or unavailable?

5. State and lifecycle:
   What happens before, during, after, retry, cancellation, expiry, invalidation,
   and recovery?

6. Failure / premortem:
   If the outcome fails in production, what are the likely causes? Add nodes for
   false positives, false negatives, stale data, missing evidence, bad UX,
   unsafe action, unreviewable output, and cost/latency collapse when relevant.

7. Inverse / red-team:
   What would prove this branch is harmful or false? What should the system
   refuse to say, refuse to execute, or explicitly mark uncertain?

8. Measurement / feedback:
   How will the system know later whether the output was correct? What sample,
   trace, snapshot, R multiple, user action, or review surface closes the loop?

9. Boundary / non-goals:
   What must not change? What should remain manual, read-only, delayed, hidden,
   or explicitly out of scope?

10. Operations / maintenance:
   What makes the capability reliable under real use: permissions, account
   scope, migrations, compatibility, observability, cost, latency, and rollout?
```

Record the audit in the outcome tree JSON when practical:

```json
{
  "coverageReview": [
    {
      "lens": "Outcome-needs chain",
      "finding": "overview_brief needs price-level plan; the overview page needs the minimal message.",
      "treeChange": "Moved action_plan under advice_center_overview_brief.",
      "residualRisk": "Chase semantics still need sample-backed calibration."
    }
  ]
}
```

Completeness does not mean adding every conceivable feature. A finding becomes
a tree node only if it can block the proof standard, corrupt the ruler, create
unsafe action, make the result unreviewable, or materially change the next
P0/P1 decision. Otherwise mark it as deferred P2/P3 or a non-goal.

## Rethink Mode

When the user asks to "重新推一遍" one node, "以 X 为果推因", "有没有漏因",
"层级错", "果因关系不顺", or explicitly says `outcomeback rethink`, switch
from whole-tree planning to single-node rethinking. Use the
`outcomeback-rethink` skill if available.

In rethink mode:

1. Freeze the rest of the tree.
2. Treat the selected node as the temporary root outcome.
3. Spend the reasoning budget on the direct child results this parent needs.
4. Compare the blank-page needs list against current children.
5. Return keep / rename / move / split / add / defer changes.
6. Patch the tree JSON and regenerate HTML only if the user asks for file
   updates or the current task is explicitly to repair the visual ledger.

This mode exists to prevent old broad LLM behavior: do not answer by producing
a general architecture essay, and do not create a backlog for unrelated
branches. The deliverable is a local outcome-needs repair for one node.

## Operating Rule

For non-trivial tasks, start with these questions before choosing an implementation:

1. What result is the user trying to achieve?
2. What domain does this result belong to, and what does "effective", "good",
   "safe", "accurate", "profitable", or "useful" mean in that domain?
3. What is the minimum domain-valid output?
4. What object or system behavior is supposed to become the "ruler" for that result?
5. What would prove the ruler works?
6. What capabilities must the system/user/process have for that proof to happen?
7. Which capabilities already exist, and which are missing or weak?
8. What is the current distance-to-goal score for each important capability?
9. Which gaps should become P0/P1/P2/P3 subtasks?
10. Which branch closes the most important gap with the least false confidence?
11. What did the coverage audit add, move, downgrade, or explicitly reject?

For simple mechanical requests, use the compact version: state the intended result in one sentence, then execute.

## Goal Ledger

When the user is pursuing a durable goal, revenue target, product target, safety target, or long-running system outcome, maintain a small goal ledger before choosing work.

If a goal tool such as `/goal` is available, use it as a ledger for the objective, budget, and completion state. Do not treat it as an automatic judge. The assistant must still define the proof standard, score progress, create subtasks, and verify evidence before marking the goal complete.

If no goal tool is available, hold the ledger in the plan or write it into the repo document the user has designated as authoritative.

For large work, prefer holding the ledger as an outcome tree JSON/HTML rather
than only in prose. The visual ledger must stay temporary and operational; do
not pollute a long-term target document with working subtasks.

### Activating a Goal From an Outcome Tree

If the user wants to start work from an outcome tree and a goal tool is
available, activate the goal with an objective that names the tree path and the
root outcome. The goal tool is only a pointer and status holder; it does not
replace the tree.

Before each work phase:

1. Read the active goal.
2. Re-open the referenced `outcome-tree.json`.
3. Identify the highest-priority weak or missing P0 node that still blocks a
   proof gate.
4. Re-read the node's parent chain so the work stays attached to the root
   outcome by explicit parent-needs-child links.
5. Implement or investigate that node only.
6. Verify the node's acceptance check.
7. Rescore or update the tree before moving to the next node.

Do not start from a stale memory of the tree. The JSON is the live ledger. If
the active goal references a missing tree file, stop and ask for the correct
ledger path or rebuild the tree.

The ledger must include:

```text
Goal:
Deadline / target number:
Current distance-to-goal score:
Proof gates:
Weakest capabilities:
Next P0-P3 subtasks:
Evidence collected:
Residual risk:
```

Do not mark a durable goal complete merely because code was written. Completion requires the proof gates to pass or the user to explicitly accept the remaining risk.

## Distance Scorecard

For strategic or high-impact work, score the system's distance to the outcome before and after implementation.

Use a 0-100 score only as a decision aid, not as false precision:

- `0-30`: the capability mostly does not exist or is unsafe to trust.
- `31-50`: partial plumbing exists, but the proof loop is missing or misleading.
- `51-70`: usable for review or limited trial, with known gaps.
- `71-85`: operationally useful, with evidence and bounded risk.
- `86-100`: strong, verified, and stable under realistic edge cases.

Score each capability separately, then state the overall distance in plain language. Prefer honest low scores over polished uncertainty.

Capability scoring template:

```text
Capability:
Current score:
Evidence:
Missing proof:
Main risk if left weak:
Next subtask:
```

If the task is about money, safety, execution, health, or user trust, never score only the model output. Also score data quality, traceability, safety boundaries, feedback/review quality, and cost/latency when relevant.

## Automatic Subtask Creation

Turn the weakest capability gaps into a prioritized subtask queue. The queue should be outcome-shaped, not file-shaped.

Priority rules:

- `P0`: blocks the proof standard, corrupts the ruler, creates unsafe action, or makes results unreviewable.
- `P1`: materially improves the main outcome but has a safe workaround.
- `P2`: improves coverage, usability, speed, or clarity after the main loop works.
- `P3`: useful polish, expansion, or research that should not block the current outcome.

Every generated subtask should include:

```text
Subtask:
Why it matters to the goal:
Input / code path / data source:
Expected output:
Acceptance check:
Owner lens:
```

When the user asks to work from P0 to Pn, do not dump a giant backlog and stop. For each phase: state the phase plan, implement or investigate it, verify it, then rescore before moving on.

## Iteration Loop

For long-running goals, use this loop:

```text
1. Re-read the goal and proof gates.
2. Score current capability distance.
3. Create or update P0-P3 subtasks from the weakest gaps.
4. Pick the highest-leverage subtask that preserves safety boundaries.
5. Implement or investigate.
6. Verify against acceptance checks.
7. Rescore and decide whether the next subtask is still the right one.
8. Stop only when proof gates pass, a blocker is real, or the user redirects.
```

When using subagents, give each agent one bounded subtask or one specialist question tied to a scorecard gap. Do not ask subagents to solve the whole goal unless the user explicitly requested a broad roundtable.

## Recursive Outcome Tree

Build a small tree before building code when the request is strategic, ambiguous, or high impact.

1. Define the outcome precisely.
   - Make it observable: business result, user behavior, decision quality, execution quality, safety, reviewability, or reliability.
   - Preserve numbers and timeframes.
   - If the user asks "can we achieve X", treat X as the root node.

2. Define the domain ruler.
   - Identify the domain lens that should judge the result: finance, medicine,
     law, sports, education, operations, security, UX, engineering, etc.
   - Translate quality words into domain terms before naming product artifacts.
   - Example: in a trading system, "effective advice" first means a financially
     actionable judgment with ticker, action, price levels, reason, evidence,
     risk/odds, invalidation, and repair path. It is not first a card, API
     field, brief, or dashboard widget.

3. Define the ruler.
   - Name what will measure progress toward the outcome.
   - Ask whether the ruler itself is measuring the right thing.
   - If the ruler is wrong, fix the ruler before tuning the system.
   - Example: a trading "static anchor" is not merely a buy-entry marker; it is a frozen future-path judgment that later measures whether the decision system saw price correctly.

4. Derive required capabilities.
   - Split the outcome into capabilities, not features.
   - Common buckets: decision quality, execution quality, feedback/review quality, safety/risk control, observability, data quality, user experience, cost/latency.
   - For each capability, ask: "Does the parent result need this child result
     at this exact layer?"
   - Also ask: "If this child is absent, how exactly does the parent fail?"
   - Give each major capability an initial score and one missing proof item.

5. Recurse to the target depth.
   - Treat each accepted non-leaf capability as a new parent result, then derive
     the direct child results it needs from scratch.
   - Default to the Recursive Depth Contract: Focused mode expands to 4 visible
     layers, Full tree mode expands to 5 visible layers, and an explicit user
     depth such as "推 9 层" overrides the default.
   - Stop early only when a node is directly actionable, has a clear proof
     check, and further splitting would not change the next action or
     verification. Mark it as a leaf with the reason.
   - If a node still reads like a slogan, recurse again.
   - If a branch jumps from visible product result to bottom data too quickly,
     insert the missing contract/capability/process node.

6. Reuse existing system strength first.
   - Inspect current code, docs, data, APIs, and local conventions before inventing new machinery.
   - Prefer existing algorithms, schemas, routes, helpers, skills, and tests when they can be extended honestly.
   - If existing support is close but semantically wrong, rename or split the boundary instead of overloading it.

7. Branch deliberately.
   - Create competing hypotheses for how to close the gap.
   - Include at least one inverse branch: "What if the premise is wrong?" or "What would make this change harmful?"
   - Use the door rule: if pulling does not work, try pushing. If the direct approach fails, examine the opposite framing.
   - Keep the default branch budget to 2-4 branches unless the user explicitly asks for a broad exploration.

8. Use specialist thinking only when it changes the tree.
   - If a missing capability requires domain reasoning, identify the specialist lens needed: finance, risk, quant, UX, data, security, ops, etc.
   - When subagents are available and the user explicitly asks for agents/delegation, spawn bounded specialist agents with one branch or question each.
   - When subagents are not appropriate, simulate the specialist lens locally and label it as local reasoning.
   - Do not delegate the next blocking step if the main work depends on it immediately.

9. Converge before implementation.
   - Compare branches against the proof standard.
   - Choose the branch that most improves the outcome while preserving hard boundaries.
   - State what is intentionally not being solved yet.
   - Convert deferred gaps into P1-P3 subtasks instead of losing them.

10. Audit completeness.
   - Run the coverage lenses after the first tree is built.
   - For each lens, either add/move a node, record a deferred risk, or state why
     the lens does not apply.
   - Pay special attention to outcome-needs mistakes: sibling nodes that should
     be parent/child, related modules that the parent does not directly need,
     and data sources masquerading as capabilities.

## Planning Shape

For substantial work, write or internally hold this plan:

```text
Outcome:
Domain:
Domain ruler:
Minimum domain-valid output:
Ruler / proof standard:
Capability tree:
- capability A -> current score -> existing support -> gap -> candidate branch -> subtask priority
- capability B -> current score -> existing support -> gap -> candidate branch -> subtask priority
Chosen branch:
Implementation targets:
Verification:
Rescore:
Residual risk:
Coverage audit:
- lens -> finding -> tree change -> residual risk
```

Use this plan to prevent activity drift. If a proposed feature does not improve a named capability, drop it or defer it.

## Implementation Discipline

During implementation:

- Inspect the actual code path before editing.
- Keep naming aligned with true semantics.
- Do not let a display label imply stronger behavior than the system guarantees.
- Preserve execution/safety boundaries when adding review-only or advisory fields.
- Add compatibility aliases when a name is wrong but already part of a public contract.
- Add comments only for boundaries and invariants, not obvious mechanics.

After implementation:

- Run tests that prove the capability, not merely line coverage.
- Check diffs for accidental behavior changes.
- Rescore the affected capability.
- Explain which outcome capability improved, which subtask was closed, and what evidence remains missing.

## Review Discipline

For reviews, lead with outcome risk:

- Which issue prevents the desired result?
- Which issue corrupts the ruler?
- Which issue can cause a false positive, false negative, unsafe action, data loss, or misleading UI?
- Which missing test leaves the outcome unproven?

Separate:

- Outcome blockers
- Ruler/measurement flaws
- Capability gaps
- Contract or data risks
- Local code defects
- Test/observability gaps

## Recursive Questions

Use these questions to keep thinking sharp:

- If this succeeds, what becomes measurably better?
- What would prove the opposite?
- Are we improving the system, or only making its output sound better?
- Is the current "ruler" measuring the true target or a convenient proxy?
- What capability must exist before this feature matters?
- Can the existing system already do 70% of this?
- What branch would we choose if the current framing were false?
- What is the smallest closed loop that can validate or falsify this branch?
- Which score is limiting the whole goal right now?
- What is the next P0/P1 subtask implied by that weak score?
- Would this subtask still matter if the visible UI or current symptom changed?

## Anti-Patterns

Avoid:

- Starting from the first visible bug before defining the target result.
- Treating a feature as progress when it does not improve a named capability.
- Mistaking a metric, label, or UI panel for the actual ruler.
- Building only the happy-path branch and skipping the inverse case.
- Calling something executable, safe, accurate, or final when it is only a reference, fallback, draft, or display snapshot.
- Delegating broad thinking to subagents without a bounded branch/question.
- Expanding scope after discovering adjacent issues unless they block the stated outcome.
- Marking a goal complete immediately after implementation without rescoring or checking proof gates.
- Producing a long task list that is not tied to capability scores or acceptance checks.
