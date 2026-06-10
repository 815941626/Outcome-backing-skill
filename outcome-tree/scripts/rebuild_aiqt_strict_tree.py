#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the AIQT overview-advice map from a local-parent-only tree.

This example is intentionally rebuilt from the current outcome-backward-working
rules. Each recursion step treats the current node as the only parent result:
children must directly make that local parent true. Memory, old trees, and
known modules are used only as evidence after the local child causes are
derived.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "aiqt-overview-advice.json"

nodes: list[dict] = []


def add(
    node_id: str,
    title: str,
    summary: str,
    parent: str | None = None,
    *,
    status: str = "partial",
    priority: str = "P0",
    score: int | None = None,
    work: str | None = None,
    lens: str | None = None,
    need_type: str | None = None,
    local: str,
    shape: str,
    need: str | None = None,
    proof: str | None = None,
    gate: str | None = None,
    domain: str | None = None,
    domain_ruler: str | None = None,
    domain_output: str | None = None,
    existing: list[str] | None = None,
    gaps: list[str] | None = None,
    risks: list[str] | None = None,
    next_step: str | None = None,
) -> None:
    node: dict = {
        "id": node_id,
        "title": title,
        "summary": summary,
        "status": status,
        "priority": priority,
        "localResult": local,
        "targetShape": shape,
    }
    if parent:
        node["parentId"] = parent
    if score is not None:
        node["score"] = score
    if work:
        node["workStatus"] = work
    if lens:
        node["ownerLens"] = lens
    if need_type:
        node["needType"] = need_type
    if need:
        node["directCauseForParent"] = need
    if proof:
        node["edgeProof"] = proof
    if gate:
        node["proofGate"] = gate
    if domain:
        node["domain"] = domain
    if domain_ruler:
        node["domainRuler"] = domain_ruler
    if domain_output:
        node["domainValidOutput"] = domain_output
    if existing:
        node["existingSupport"] = existing
    if gaps:
        node["gaps"] = gaps
    if risks:
        node["risks"] = risks
    if next_step:
        node["nextSubtask"] = next_step
    nodes.append(node)


root = "outcome:overview-effective-advice"
compressed_advice = "product:overview-compressed-effective-advice"
domain_advice = "domain:finance-valid-action-advice"
visible_summary = "visible:overview-first-screen-delivery"
safety_trace = "proof:safety-trace-reviewable"
price_plan = "plan:price-level-trade-plan"
action_validity = "judgment:current-action-validity"
entry_rule = "rule:entry-trigger-max-chase"
worth_judgment = "judgment:plan-worth-doing"


add(
    root,
    "结果：总览页有有效建议",
    "骑手打开总览页后，第一屏看到一条压缩后仍然有效的金融建议。",
    status="target",
    score=38,
    work="active",
    lens="finance/product",
    need_type="outcome",
    domain="finance",
    domain_ruler="有效建议 = 金融上可行动、可放弃、可复盘、能解释风险和把握的判断。",
    domain_output=(
        "总览第一屏压缩建议必须保留 <ticker>、<action>、<price_boundary>、"
        "<confidence_or_sample_state>、<repair>、<evidence_compact>、<manual_boundary>。"
    ),
    local="总览页这个结果成立：用户第一屏看到的是压缩后仍可行动、可放弃、可复盘的建议。",
    shape=(
        "模拟，不是投资建议：<ticker>｜<action_label>｜"
        "<entry_or_trigger> 才做，超过 <max_entry_or_not_applicable> 放弃｜"
        "目标/退出 <target_or_exit>，失效 <stop_or_invalidation>｜"
        "把握 <probability_or_sample_insufficient>｜错后 <first_repair_action>｜"
        "证据 <evidence_compact>｜边界 <manual_preflight_required>。"
    ),
    gate="总览页展示的压缩建议必须来自完整有效建议，且压缩后不丢关键行动边界。",
    existing=[
        "项目已有总览页、建议中心、部分 overview brief/minimal message 接口。",
        "本图按 Local Parent Only 重推，每层只服务最近父节点。",
    ],
    gaps=[
        "当前系统是否真的能产出金融上有效的行动建议，需要逐节点用代码和数据核对。",
        "价格级计划、把握校准、错后补救仍是 P0 弱点。",
    ],
)


# Root direct children. These are only the direct causes needed for the root:
# the compressed advice product exists, it is delivered on the first screen,
# and it keeps the safety/proof boundary.
add(
    compressed_advice,
    "产物：总览压缩后有效建议",
    "总览页真正展示的是完整有效建议的压缩版；它短，但不能丢行动边界。",
    root,
    score=30,
    lens="finance/product",
    need_type="outcome",
    domain="finance",
    domain_ruler="压缩后仍有效 = 读起来短，但仍保留动作、价位、把握、错后、证据和人工边界。",
    domain_output=(
        "<ticker>；<action_label>；<entry_or_trigger>；<stop_or_invalidation>；"
        "<target_or_exit>；<confidence_or_sample_state>；<repair>；"
        "<evidence_compact>；<manual_boundary>。"
    ),
    local="存在一条可被总览直接展示的压缩后有效建议。",
    shape=(
        "模拟压缩建议：<ticker>｜<action_label>｜<entry_or_trigger>/<stop_or_invalidation>/<target_or_exit>｜"
        "<confidence_or_sample_state>｜<repair>｜<evidence_compact>｜<manual_boundary>。"
    ),
    need="没有压缩后有效建议这个产物，root 只能是空页面或长报告入口。",
    proof="父结果说的是总览页有有效建议；直接需要一个能放到总览上的有效建议产物。",
    gate="压缩结果不能自造 verdict，不能丢掉价格边界和风险边界。",
)

add(
    domain_advice,
    "来源：完整金融有效建议",
    "压缩建议必须来自一条完整金融有效建议，而不是总览页自己临时拼判断。",
    "source:summary-from-domain-advice",
    score=28,
    lens="finance",
    need_type="domain_result",
    domain="finance",
    domain_ruler="可行动、可放弃、可复盘，并能解释风险收益和判断把握。",
    domain_output=(
        "<ticker>；<buy/sell/wait/avoid>；<entry_or_trigger>；<max_entry>；"
        "<stop_or_invalidation>；<target_or_exit>；<why>；<evidence>；"
        "<confidence>；<repair>。"
    ),
    local="存在一条可被压缩的完整金融行动建议。",
    shape=(
        "模拟金融建议：<ticker> <action>；<entry_or_trigger> 才行动；"
        "超过 <max_entry_or_not_applicable> 不追；跌破/触发 <stop_or_invalidation> 失效；"
        "目标/退出 <target_or_exit>；理由 <why_buy_sell_wait>；"
        "证据 <evidence_compact>；把握 <probability_or_sample_insufficient>；"
        "错后 <first_repair_action>。"
    ),
    need="没有完整有效建议，来源节点就只是一个空引用。",
    proof="当前父节点是压缩建议来源；它直接需要一条完整金融有效建议。",
    gate="建议必须回答标的、动作、价格、理由、把握、错后、证据和失效条件。",
)

add(
    visible_summary,
    "交付：总览第一屏呈现这条压缩建议",
    "压缩建议成立后，必须在总览第一屏被用户直接看到。",
    root,
    score=42,
    lens="UX",
    need_type="visible_acceptance",
    local="总览第一屏展示这条压缩建议。",
    shape=(
        "模拟第一屏：主标题 <ticker_action>；一句话 <why_now_and_plan>；"
        "价位 <entry_stop_target>；把握 <confidence_label>；错后 <repair_line>；"
        "边界 <manual_preflight_badge>。"
    ),
    need="压缩建议存在但不在总览第一屏呈现，root 的“总览页有”不成立。",
    proof="当前父节点是总览页结果；它直接需要第一屏承载。",
    gate="第一屏必须看到同一条压缩建议，而不是第二套推荐文案。",
)

add(
    safety_trace,
    "证明：建议安全、可追溯、可复盘",
    "有效建议不能只看起来像建议，还要知道依据、时效、边界和后验结果。",
    root,
    score=34,
    lens="risk/review",
    need_type="evidence",
    local="每条建议能追溯到当时数据，且不会越权执行。",
    shape=(
        "模拟证明：source_ref=<source_ref>，snapshot_ref=<snapshot_ref>，"
        "freshness=<fresh_or_stale>，execution=<manual_preflight_required>，"
        "later_review=<review_status_or_pending>。"
    ),
    need="没有安全和追溯，建议可能误导、越权或无法复盘。",
    proof="父结果中的“有效”包含安全和可验证，不只是文本命中。",
    gate="真实账户只读；关键输入有 freshness；建议可被冻结后复盘。",
)


# Complete finance advice children. These are mechanisms, not a flat field list.
add(
    price_plan,
    "计划：价格级交易计划",
    "完整金融建议首先要给出用户能行动的价格计划。",
    domain_advice,
    score=22,
    lens="trading",
    need_type="outcome",
    local="存在一份可执行、可放弃、可失效的价格级交易计划。",
    shape=(
        "模拟计划：subject=<ticker>，action=<action>，entry_or_trigger=<entry_or_trigger>，"
        "max_entry=<max_entry_or_not_applicable>，stop_or_invalidation=<stop_or_invalidation>，"
        "target_or_exit=<target_or_exit>，abandon_if=<abandon_condition>。"
    ),
    need="没有价格级交易计划，完整建议只有观点，不能行动。",
    proof="当前父节点是完整金融有效建议；它直接需要一份可执行计划。",
    gate="任何 buy/chase/sell 都必须有价格边界或明确不适用原因。",
)

add(
    worth_judgment,
    "判断：这笔计划值得做",
    "有计划还不够，还要证明风险收益和把握值得执行。",
    domain_advice,
    score=18,
    lens="quant/finance",
    need_type="judgment",
    local="给出 plan_quality、confidence_state、risk_reward_state。",
    shape=(
        "模拟判断：plan_quality=<worth_doing_or_wait_or_block>，"
        "confidence=<calibrated_probability_or_sample_insufficient>，"
        "risk_reward=<acceptable_or_unknown_or_bad>。"
    ),
    need="没有值得做的判断，价格计划可能只是可执行但不该执行。",
    proof="当前父节点是有效建议；有效不只是能做，还要值得做。",
    gate="把握不足、赔率不清或风险收益差时降级。",
)

add(
    "domain:repair-if-wrong",
    "策略：判断错了有补救路径",
    "完整金融建议必须预先说明错了第一步怎么处理。",
    domain_advice,
    score=22,
    lens="risk",
    need_type="judgment",
    local="给出 first_repair_action。",
    shape="模拟补救：if_wrong=<first_repair_action>，trigger=<repair_trigger>，no_average_down=<boundary>。",
    need="没有错后补救，完整建议只说进攻不说防守。",
    proof="当前父节点是完整有效建议；有效建议需要能处理判断失败。",
    gate="补救动作不扩大风险，不绕过 preflight。",
)


# Price-level trade plan children.
add(
    "domain:ticker-action-verdict",
    "机制：标的和动作被锁定",
    "价格计划必须先锁定计划对象和动作，不能一边计划一边换结论。",
    price_plan,
    score=34,
    lens="finance",
    need_type="judgment",
    local="锁定 <ticker> 和 <action>。",
    shape="模拟锁定：subject=<ticker>，action=<buy_sell_wait_avoid>，action_reason_ref=<reason_ref>。",
    need="没有标的和动作，价格计划不知道给谁、做什么。",
    proof="当前父节点是价格级交易计划；计划需要对象和动作被锁定。",
    gate="观察/等待/避开不能被包装成买入。",
)

add(
    action_validity,
    "判断：当前动作成立",
    "价格计划要成立，必须先判断当前动作为什么成立或为什么要等。",
    price_plan,
    score=20,
    lens="research/trading",
    need_type="judgment",
    local="给出 action_validity=<valid_wait_block> 和 why_now。",
    shape="模拟判断：action_validity=<valid_or_wait_or_block>，why=<why_buy_sell_wait>，evidence_state=<support_conflict_unknown>。",
    need="没有当前动作成立判断，价格计划只是机械价位表。",
    proof="当前父节点是交易计划；计划的价格边界必须服务于一个成立的动作判断。",
    gate="动作不成立时，计划降级为等待/观察/放弃。",
)

add(
    entry_rule,
    "规则：入场/触发/最高追",
    "价格计划要说明什么时候开始做、最高追到哪里。",
    price_plan,
    score=18,
    lens="trading",
    need_type="process",
    local="给出 entry_or_trigger、max_entry、abandon_if。",
    shape="模拟规则：entry_or_trigger=<entry_or_trigger>，max_entry=<max_entry>，abandon_if=<abandon_condition>。",
    need="没有入场和最高追规则，计划无法回答怎么追或何时放弃。",
    proof="当前父节点是价格级交易计划；它直接需要入场边界。",
    gate="追高必须同时有触发、上限和失效条件。",
)

add(
    "model:risk-reward-levels",
    "规则：止损/失效/目标",
    "价格计划要说明错到哪里失效、对到哪里退出。",
    price_plan,
    score=24,
    lens="risk",
    need_type="process",
    local="生成 stop_or_invalidation 和 target_or_exit。",
    shape="模拟输出：stop_or_invalidation=<stop_or_invalidation>，target_or_exit=<target_or_exit>，risk_unit=<risk_unit>。",
    need="没有止损/失效/目标，父计划不能称为交易计划。",
    proof="当前父节点是价格级交易计划；它直接需要防守和退出边界。",
    gate="缺 stop/target 时 buy/chase 降级。",
)

add(
    "rule:abandon-condition",
    "规则：放弃条件",
    "价格计划要说明什么情况不做，防止追着错误计划跑。",
    price_plan,
    score=28,
    lens="risk",
    need_type="safety",
    local="给出 abandon_if。",
    shape="模拟规则：abandon_if=<price_miss_or_signal_fail_or_data_stale_condition>。",
    need="没有放弃条件，价格计划会变成无限等待或无限追。",
    proof="当前父节点是可放弃的交易计划；它直接需要放弃边界。",
    gate="触发放弃条件时不输出强动作。",
)


# Current action validity children.
add(
    "domain:why-now-evidence",
    "机制：为什么现在这个动作成立",
    "动作成立要说明现在的局面为什么支持买、卖、等或避开。",
    action_validity,
    score=26,
    lens="research",
    need_type="judgment",
    local="给出 why_buy_sell_wait 和证据摘要。",
    shape=(
        "模拟理由：why=<why_buy_sell_wait>，thesis=<support_conflict_unknown>，"
        "news=<support_conflict_unknown>，kline=<support_conflict_unknown>。"
    ),
    need="没有 why 和证据，当前动作只是结论，不是可判断动作。",
    proof="当前父节点是动作成立判断；它直接需要成立理由。",
    gate="证据冲突或未知必须降级。",
)

add(
    "data:current-price-location",
    "数据：当前价格位置",
    "动作成立必须知道当前价格相对计划和关键位的位置。",
    action_validity,
    score=30,
    priority="P1",
    lens="data",
    need_type="data",
    local="提供 current_price 与 trigger/support/resistance 的关系。",
    shape="模拟数据：current_price=<current_price>，relative_to_trigger=<above_or_below>，relative_to_plan=<cheap_ok_expensive>。",
    need="没有当前价格位置，无法判断现在能不能追、等或放弃。",
    proof="当前父节点是当前动作成立；它直接依赖当前价格位置。",
    gate="价格位置缺失时显示延迟/等待。",
)

add(
    "process:situation-judgment",
    "处理：thesis/news/K线局面判断",
    "为什么现在成立需要把三源证据合成局面判断。",
    "domain:why-now-evidence",
    score=28,
    lens="research",
    need_type="process",
    local="生成 support/conflict/unknown 和 why。",
    shape="模拟输出：thesis=<support_conflict_unknown>，news=<support_conflict_unknown>，kline=<support_conflict_unknown>，why=<why_line>。",
    need="没有局面判断，父理由只有材料没有机制。",
    proof="当前父节点是 why_now 机制；它需要证据合成。",
    gate="三源冲突时显示冲突并降级。",
)

add(
    "rule:evidence-conflict",
    "规则：证据冲突/未知降级",
    "动作成立判断必须处理证据冲突和未知，不能强行写成支持。",
    action_validity,
    score=26,
    priority="P1",
    lens="research",
    need_type="process",
    local="处理 support/conflict/unknown。",
    shape="模拟规则：if core_evidence=<conflict_or_unknown> then action_validity=<wait_or_block> and reason=<conflict_reason>。",
    need="没有冲突处理，当前动作成立判断可能误导。",
    proof="当前父节点是动作成立判断；冲突/未知直接影响动作是否成立。",
    gate="冲突时不输出无保留强建议。",
)

add(
    "data:thesis-news-kline",
    "底部数据：thesis/news/K线三源",
    "局面判断需要基本面逻辑、消息和价格结构。",
    "process:situation-judgment",
    score=36,
    priority="P1",
    lens="research",
    need_type="data",
    local="提供 thesis_ref、news_ref、kline_ref。",
    shape="模拟数据：thesis_ref=<thesis_ref>，news_ref=<news_ref>，kline_ref=<kline_ref>，freshness=<freshness_state>。",
    need="没有三源材料，父过程没有证据来源。",
    proof="当前父节点是局面判断；它直接需要三源材料。",
    gate="缺失材料标 unknown，不假装支持。",
)


# Entry/trigger rule children.
add(
    "model:entry-chase-pullback",
    "模型：追高/回踩/禁止追",
    "入场规则要区分现在能追、等回踩还是放弃。",
    entry_rule,
    score=18,
    lens="trading",
    need_type="process",
    local="生成 chase/wait/block 分类。",
    shape="模拟输出：classification=<chase_or_wait_pullback_or_block>，trigger=<trigger_condition>，max_entry=<max_entry>，abandon_if=<abandon_condition>。",
    need="没有这个模型，父规则无法回答怎么追。",
    proof="当前父节点是入场/触发/最高追；它直接需要追高/回踩判断。",
    gate="追高必须同时有触发、上限和失效条件。",
)

add(
    "data:plan-anchor",
    "底部数据：计划锚点",
    "追高/回踩要基于冻结计划，而不是临时拿当前价当买点。",
    "model:entry-chase-pullback",
    score=42,
    lens="data",
    need_type="data",
    local="提供 entry_anchor/trigger/stop/target。",
    shape="模拟数据：entry_anchor=<entry_anchor>，trigger=<trigger>，stop=<stop>，target=<target>，source_ref=<plan_source_ref>。",
    need="没有计划锚点，父模型无法判断价格是否追过头。",
    proof="追高/回踩是相对计划的判断。",
    gate="锚点缺失时只能观察或等待。",
)

add(
    "data:daily-kline",
    "底部数据：日线/K线结构",
    "价格模型需要近期走势、支撑、压力和量能。",
    "model:entry-chase-pullback",
    score=58,
    priority="P1",
    lens="data",
    need_type="data",
    local="提供 OHLCV、前高、支撑、量价结构。",
    shape="模拟数据：bars=<ohlcv_series>，prior_high=<prior_high>，support=<support_zone>，volume_state=<volume_state>。",
    need="没有 K 线结构，父模型无法区分突破和冲高回落。",
    proof="追高/回踩直接依赖价格路径。",
    gate="K线不可用时不输出结构判断。",
)

add(
    "data:intraday-tape",
    "底部数据：分时价格/量能",
    "追高判断需要当前盘中位置和量价状态。",
    "model:entry-chase-pullback",
    score=30,
    priority="P1",
    lens="data",
    need_type="data",
    local="提供 current_price、VWAP、量能和关键位关系。",
    shape="模拟数据：current_price=<current_price>，vwap=<vwap>，relative_to_trigger=<above_or_below>，volume_state=<volume_state>。",
    need="没有分时状态，父模型不能判断现在是否可以追。",
    proof="追高是当前时点判断。",
    gate="分时缺失时显示延迟/等待。",
)


# Plan-worth children.
add(
    "domain:confidence-odds",
    "机制：把握和赔率支持执行",
    "这笔计划值得做，需要表达把握、样本状态和赔率是否匹配。",
    worth_judgment,
    score=20,
    lens="quant",
    need_type="judgment",
    local="给出 confidence_label、sample_state、risk_reward。",
    shape=(
        "模拟把握：confidence=<calibrated_probability_or_sample_insufficient>，"
        "risk_reward=<risk_reward_or_unknown>，caveat=<confidence_caveat>。"
    ),
    need="没有把握和赔率，父判断无法说明这笔计划值不值得做。",
    proof="当前父节点是计划值得做；它直接需要把握和赔率机制。",
    gate="样本不足不显示伪精确胜率；赔率不清时不升级强动作。",
)

add(
    "rule:honest-confidence-label",
    "规则：诚实把握口径",
    "样本不足时不能显示伪精确概率。",
    "domain:confidence-odds",
    score=44,
    lens="quant",
    need_type="safety",
    local="区分 calibrated 与 sample_insufficient。",
    shape="模拟规则：if sample_state=<insufficient> then confidence=<sample_insufficient> and probability=<none>。",
    need="没有诚实口径，父把握会误导用户。",
    proof="概率/胜率必须先避免伪确定性。",
    gate="未校准不输出数值胜率。",
)

add(
    "process:probability-calibration",
    "处理：同类样本概率校准",
    "要给概率数值，必须来自同类 setup 后验样本。",
    "domain:confidence-odds",
    score=16,
    lens="quant",
    need_type="process",
    local="生成 calibrated_probability 或 insufficient。",
    shape="模拟输出：setup_bucket=<setup_bucket>，sample_size=<sample_size_or_insufficient>，hit_rate=<calibrated_rate_or_none>，expected_r=<expected_r_or_unknown>。",
    need="没有校准过程，父把握只能是结构置信。",
    proof="数值概率需要统计来源。",
    gate="样本不足时不显示概率。",
)

add(
    "data:closed-loop-samples",
    "后验数据：建议闭环样本",
    "概率校准需要过去建议之后的结果。",
    "process:probability-calibration",
    score=28,
    priority="P1",
    lens="review_loop",
    need_type="feedback",
    local="提供 frozen advice 和后验结果。",
    shape="模拟样本：advice_ref=<advice_ref>，horizon=<review_horizon>，outcome=<hit_miss_unclear>，r_multiple=<r_multiple_or_unknown>。",
    need="没有后验样本，父过程没有依据。",
    proof="校准不是主观 confidence。",
    gate="样本必须回到当时快照。",
)

add(
    "data:setup-regime-tags",
    "数据：setup/市场环境分桶",
    "同类概率需要分桶，不能混样本。",
    "process:probability-calibration",
    score=22,
    priority="P1",
    lens="quant",
    need_type="data",
    local="提供 setup_bucket/regime/liquidity。",
    shape="模拟标签：setup=<setup_bucket>，regime=<market_regime>，liquidity=<liquidity_state>。",
    need="没有分桶，父过程会制造假概率。",
    proof="概率校准要比较同类。",
    gate="无分桶时只显示未校准。",
)


# Repair children.
add(
    "rule:repair-taxonomy",
    "规则：补救动作枚举",
    "错后补救要稳定可测。",
    "domain:repair-if-wrong",
    score=30,
    lens="risk",
    need_type="contract",
    local="定义 cancel/stop_chase/reduce/exit/wait_reassess 等动作。",
    shape="模拟枚举：repair_action=<cancel_or_stop_chase_or_reduce_or_exit_or_wait_reassess>。",
    need="没有枚举，父策略会变成随意说明文。",
    proof="补救动作必须可审查。",
    gate="动作必须来自固定集合。",
)

add(
    "data:invalidation-state",
    "数据：计划失效状态",
    "补救策略需要知道原判断何时失效。",
    "domain:repair-if-wrong",
    score=30,
    lens="risk",
    need_type="data",
    local="提供 abandon_if/invalidation 是否触发。",
    shape="模拟数据：invalidation=<triggered_or_not>，condition=<invalidation_condition>，price_relation=<relation_to_key_level>。",
    need="没有失效状态，父策略不知道何时判错。",
    proof="错后补救由失效条件触发。",
    gate="没有失效条件时不输出强建议。",
)

add(
    "data:position-risk-preflight",
    "数据：持仓/风险/preflight",
    "补救动作取决于是否持仓和风险状态。",
    "domain:repair-if-wrong",
    score=42,
    lens="risk",
    need_type="data",
    local="提供 position_state/risk_state/preflight_state。",
    shape="模拟数据：position_state=<flat_or_holding>，risk_state=<risk_ok_or_blocked>，preflight=<allowed_or_blocked_with_reason>。",
    need="没有持仓风险状态，父策略无法决定退出、减仓或等待。",
    proof="错后补救不能脱离真实风险。",
    gate="不绕过 preflight。",
)

add(
    "boundary:no-average-down",
    "边界：禁止默认摊平",
    "判断错了不能默认越跌越买。",
    "domain:repair-if-wrong",
    score=38,
    lens="risk",
    need_type="safety",
    local="明确 no_average_down_unless。",
    shape="模拟边界：average_down=<blocked_unless_new_valid_advice_and_preflight>。",
    need="没有这个边界，父策略可能扩大亏损。",
    proof="补救首先是控制损失。",
    gate="新有效建议和 preflight 未通过时不建议补仓。",
)


# First-screen delivery children. These only explain why the compressed advice
# is visible on the overview page; they do not prove the finance advice itself.
add(
    "display:summary-slots",
    "展示：压缩建议有固定信息槽",
    "第一屏承载压缩建议，需要固定展示动作、价位、把握、错后、证据、边界。",
    visible_summary,
    score=40,
    lens="UX",
    need_type="output",
    local="总览第一屏有稳定可见槽位。",
    shape="模拟槽位：headline=<ticker_action>，plan=<price_plan>，confidence=<confidence_label>，repair=<repair_line>，evidence=<evidence_line>，boundary=<boundary_badge>。",
    need="没有固定槽位，压缩建议无法稳定呈现在第一屏。",
    proof="当前父节点是第一屏呈现；它直接需要可见槽位。",
    gate="槽位缺失时显示缺失或降级。",
)

add(
    "source:summary-from-domain-advice",
    "来源：压缩建议来自完整有效建议",
    "压缩建议必须引用完整有效建议，不允许总览页自己重新判断。",
    compressed_advice,
    score=34,
    lens="architecture",
    need_type="contract",
    local="overview_compressed_advice 有 domain_advice_ref。",
    shape="模拟来源：compressed.source=<domain_advice_ref>，source_kind=<complete_domain_advice>。",
    need="没有完整有效建议来源，当前父节点的压缩建议无法证明“有效”。",
    proof="当前父节点是压缩后有效建议；它直接需要完整建议来源。",
    gate="总览不二次计算正式 action，只引用来源。",
)

add(
    "display:first-screen-placement",
    "承载：第一屏主位置展示",
    "总结必须放在用户第一眼能看到的位置。",
    visible_summary,
    score=36,
    lens="frontend",
    need_type="UX",
    local="summary_advice 是总览第一屏主内容。",
    shape="模拟页面：primary_panel=<summary_advice>，secondary_panels=<risk_readiness_details>。",
    need="总结存在但不在第一屏，父结果不成立。",
    proof="父结果强调总览页第一屏能读懂。",
    gate="旧面板不能抢主位。",
)

add(
    "state:no-advice-reason",
    "边界：无有效建议时不伪造建议",
    "没有完整有效建议时，系统必须说明不能建议，而不是硬凑一条。",
    safety_trace,
    score=32,
    lens="UX",
    need_type="UX",
    local="无有效建议时显示 blocked/insufficient/stale 原因。",
    shape="模拟空态：status=<blocked_or_insufficient_or_stale>，reason=<missing_reason>，next_input=<needed_input>。",
    need="没有这个边界，安全证明无法排除伪建议。",
    proof="当前父节点是安全可追溯证明；它直接需要无建议时的 fail-closed 行为。",
    gate="关键数据缺失/过期/冲突时不显示伪确定建议。",
)

add(
    "contract:summary-advice-object",
    "合同：压缩建议字段",
    "压缩建议需要稳定字段承载关键行动信息。",
    compressed_advice,
    score=32,
    lens="architecture",
    need_type="contract",
    local="存在 overview_compressed_advice_v0。",
    shape="模拟对象：headline=<headline>，one_line=<one_line>，price_plan=<price_plan>，confidence=<confidence>，repair=<repair>，evidence=<evidence>，boundary=<boundary>。",
    need="没有字段合同，当前父节点无法稳定产出压缩建议。",
    proof="当前父节点是压缩建议产物；它直接需要字段合同。",
    gate="字段缺失时降级，不让页面补判。",
)

add(
    "process:summary-compression",
    "处理：完整建议压缩成总览建议",
    "把完整金融建议压缩成第一屏可读的一句话和标签。",
    compressed_advice,
    score=28,
    lens="UX",
    need_type="process",
    local="从完整金融有效建议生成 overview_compressed_advice。",
    shape="模拟压缩：domain_advice(<action>,<price_plan>,<why>,<confidence>,<repair>,<evidence>,<boundary>) -> summary_advice。",
    need="没有压缩过程，当前父节点只能是完整长建议，不能成为总览压缩建议。",
    proof="当前父节点是压缩建议产物；它直接需要压缩处理。",
    gate="压缩只选字段，不重新计算 verdict。",
)

add(
    "rule:compression-keeps-action-boundary",
    "规则：压缩不丢行动边界",
    "压缩后仍要保留动作、价格、把握、错后和人工边界。",
    compressed_advice,
    score=24,
    lens="finance/product",
    need_type="safety",
    local="定义压缩后必须保留的不可丢字段。",
    shape=(
        "模拟规则：required_after_compression="
        "<action,entry_or_trigger,stop_or_invalidation,target_or_exit,confidence,repair,boundary>。"
    ),
    need="没有这个规则，当前父节点可能变成好看的短文案但不再有效。",
    proof="当前父节点要求压缩后仍有效；关键行动边界不能被压缩掉。",
    gate="缺关键边界时显示不完整/降级，不输出强建议。",
)


# Safety / trace / review.
add(
    "data:freshness-timestamps",
    "数据：输入新鲜度",
    "安全证明需要知道价格、消息、判断是否过期。",
    safety_trace,
    score=42,
    lens="ops",
    need_type="data",
    local="提供 generated_at/as_of/stale。",
    shape="模拟数据：generated_at=<generated_at>，price_as_of=<price_as_of>，news_as_of=<news_as_of>，stale=<true_or_false>。",
    need="没有新鲜度，建议可能用旧数据冒充当前判断。",
    proof="有效建议必须知道时效。",
    gate="过期时降级。",
)

add(
    "trace:decision-snapshot",
    "追溯：建议和输入快照",
    "复盘需要冻结当时建议和依据。",
    safety_trace,
    score=34,
    lens="review_loop",
    need_type="evidence",
    local="提供 source_ref/snapshot_ref/hash。",
    shape="模拟追溯：advice_ref=<advice_ref>，input_snapshot_ref=<input_snapshot_ref>，hash=<snapshot_hash>。",
    need="没有快照，父证明无法知道当时系统说了什么。",
    proof="可复盘需要冻结事实。",
    gate="展示建议时保存或引用快照。",
)

add(
    "boundary:manual-execution",
    "边界：只读建议和人工 preflight",
    "总览建议不能变成自动订单。",
    safety_trace,
    score=58,
    lens="risk",
    need_type="safety",
    local="明确 review_only/manual_preflight_required。",
    shape="模拟边界：auto_order=false，preflight_required=<true_or_false>，manual_confirm=<required>。",
    need="没有执行边界，父结果可能越权。",
    proof="真实账户必须只读和人工确认。",
    gate="summary 不触发真实订单。",
)

add(
    "review:outcome-observation",
    "复盘：后验结果观察",
    "有效建议最终要能被结果检验。",
    safety_trace,
    score=30,
    priority="P1",
    lens="review_loop",
    need_type="feedback",
    local="记录建议后的价格路径或交易结果。",
    shape="模拟观察：advice_ref=<advice_ref>，horizon=<review_horizon>，outcome=<hit_miss_unclear>，lesson=<iteration_note>。",
    need="没有后验观察，父结果无法证明建议质量。",
    proof="有效性要能闭环迭代。",
    gate="未知结果标 unclear，不强行命中。",
)


subtasks = [
    {
        "priority": "P0",
        "title": "机制化完整金融建议",
        "why": "避免把完整建议拆成字段表；先固定让建议成立的机制链。",
        "input": "price_plan, worth_judgment, repair_strategy, evidence_boundary",
        "output": "domain_valid_advice_mechanism_v0",
        "acceptance": "每条建议先有价格级交易计划、值得做判断和错后补救。",
        "ownerLens": "finance",
        "workStatus": "next",
    },
    {
        "priority": "P0",
        "title": "价格级行动计划",
        "why": "有效建议必须落到买卖/追高/放弃的价格边界，并由动作成立判断支撑。",
        "input": "current_action_validity, plan anchor, daily K line, intraday tape, stop/target levels",
        "output": "entry_or_trigger/max_entry/stop_or_invalidation/target_or_exit/abandon_if",
        "acceptance": "强动作缺动作成立判断或关键价位时降级。",
        "ownerLens": "trading",
        "workStatus": "next",
    },
    {
        "priority": "P0",
        "title": "把握校准和诚实口径",
        "why": "不能把主观 confidence 包装成成功概率。",
        "input": "closed-loop samples, setup/regime tags",
        "output": "calibrated_probability or sample_insufficient",
        "acceptance": "样本不足时不显示数值概率。",
        "ownerLens": "quant",
        "workStatus": "next",
    },
    {
        "priority": "P0",
        "title": "总览第一屏总结承载",
        "why": "金融建议成立后，还要被总览页第一屏读懂。",
        "input": "domain_valid_advice_v0, summary_advice_v0, display slots",
        "output": "overview first-screen summary",
        "acceptance": "第一屏展示动作、价位、把握、错后、证据和边界。",
        "ownerLens": "UX",
        "workStatus": "next",
    },
]


def compute_metrics() -> dict:
    status_counts: dict[str, int] = {}
    work_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}
    scores: list[int] = []
    for node in nodes:
        status_counts[node["status"]] = status_counts.get(node["status"], 0) + 1
        priority_counts[node["priority"]] = priority_counts.get(node["priority"], 0) + 1
        if node.get("workStatus"):
            work_counts[node["workStatus"]] = work_counts.get(node["workStatus"], 0) + 1
        if isinstance(node.get("score"), int):
            scores.append(node["score"])
    return {
        "nodeCount": len(nodes),
        "statusCounts": status_counts,
        "workCounts": work_counts,
        "priorityCounts": priority_counts,
        "averageScore": round(sum(scores) / len(scores), 1) if scores else None,
    }


data = {
    "version": "1.0.0-mechanism-cause-overview-advice",
    "project": {
        "name": "AI Quant Trader / Mechanism Cause Outcome Map",
        "description": "按字面是入口、机制才是因重推：字段只作探针，入树的是让父果成立的机制。",
    },
    "generationMode": {
        "cleanRoom": True,
        "domainRulerFirst": True,
        "localParentOnly": True,
        "memoryClean": True,
        "mechanismNotField": True,
        "doesNotReadPreviousTree": True,
        "rule": "Literal text is an entry, decomposition is a probe, mechanism is the cause.",
    },
    "goal": {
        "title": "系统在总览页有有效建议",
        "summary": "总览第一屏展示一条压缩后仍然有效的金融建议。",
    },
    "mapLayers": [
        "最终结果",
        "直接子因：压缩建议/第一屏交付/安全证明",
        "压缩建议组成",
        "完整建议机制：价格计划/值得做/错后补救",
        "交易计划机制：动作成立/入场/止损/放弃",
        "判断机制/处理",
        "底部数据/追溯/反馈",
    ],
    "proofGates": [
        "字面是入口，不是原因；拆解是探针，不是证据；机制才是因。",
        "每层只问当前父节点要成立需要什么直接子因，不用祖先分类套子节点。",
        "root 第一层只包含总览压缩建议、第一屏交付、安全证明这三个直接子因。",
        "压缩建议必须来自完整金融有效建议，不能自造 verdict。",
        "完整金融建议先需要价格级交易计划、计划值得做、错后补救，而不是平铺字段。",
        "价格级交易计划再需要当前动作成立、入场/最高追、止损/目标、放弃条件。",
        "总览第一屏只交付同一条压缩建议，不二次裁判。",
        "样本不足、证据冲突、数据过期或缺关键价位时必须降级。",
        "真实账户只读，执行仍需 preflight 和人工确认。",
    ],
    "coverageReview": [
        {
            "lens": "Local parent only",
            "finding": "旧树会把 root 的领域/可见/证明分类继续套到后代节点，导致跨层串因。",
            "treeChange": "root 下先放总览压缩建议；完整金融建议移动到压缩建议的来源下面。",
            "residualRisk": "仍需逐节点用 outcomeback-rethink 审查是否还有错层。",
        },
        {
            "lens": "Mechanism not field",
            "finding": "旧树把完整金融建议拆成标的/动作/为什么/把握等字段，像字段表，不像果因树。",
            "treeChange": "完整建议下改成价格级交易计划、计划值得做、错后补救；为什么现在下沉到当前动作成立下面。",
            "residualRisk": "仍需继续用 rethink 审查每个机制是否真是最近父节点的直接因。",
        },
        {
            "lens": "Domain ruler",
            "finding": "业务果不能偏成产品壳，但产品壳也不能和完整金融建议混成同一层。",
            "treeChange": "压缩建议作为总览产物，完整金融有效建议作为它的来源子因。",
            "residualRisk": "仍需用真实代码核对每个金融字段当前是否能产出。",
        },
        {
            "lens": "Visible acceptance",
            "finding": "总览第一屏交付只证明压缩建议出现在总览页，不负责证明金融建议本身。",
            "treeChange": "第一屏节点只保留位置和展示槽位；来源/合同/压缩过程移到压缩建议产物下。",
            "residualRisk": "页面旧路径是否二次裁判仍需代码验证。",
        },
        {
            "lens": "Clean target shape",
            "finding": "模拟样例只描述输出形态，不承载真实行情、价格或胜率。",
            "treeChange": "全部 targetShape 使用 <placeholder>。",
            "residualRisk": "真实实现时必须由运行时数据填充并追溯。",
        },
    ],
    "nodes": nodes,
    "subtasks": subtasks,
    "metrics": compute_metrics(),
}


def validate() -> None:
    ids = {node["id"] for node in nodes}
    roots = [node for node in nodes if not node.get("parentId")]
    bad_parent = [
        (node["id"], node.get("parentId"))
        for node in nodes
        if node.get("parentId") and node["parentId"] not in ids
    ]
    missing_shape = [node["id"] for node in nodes if not node.get("targetShape")]
    root_children = [node["id"] for node in nodes if node.get("parentId") == root]
    required_root_children = {compressed_advice, visible_summary, safety_trace}
    if (
        len(roots) != 1
        or bad_parent
        or missing_shape
        or not required_root_children.issubset(root_children)
    ):
        raise SystemExit(
            "invalid tree: "
            f"roots={roots}, bad_parent={bad_parent}, "
            f"missing_shape={missing_shape}, root_children={root_children}"
        )


validate()
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT} with {len(nodes)} nodes and {len(subtasks)} subtasks")
