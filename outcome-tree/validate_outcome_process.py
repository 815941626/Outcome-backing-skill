#!/usr/bin/env python3
"""Validate an outcome-backward process JSON artifact.

This is intentionally stricter than the visual outcome-tree renderer. It checks
that the model actually built a recursive parent-needs-child process instead of
only producing a plausible-looking outline.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


DEFAULT_SCHEMA = Path(__file__).with_name("outcome_backward_process.schema.json")


class ValidationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValidationError("top-level JSON must be an object")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_shape(data: dict[str, Any]) -> None:
    required = [
        "schema_version",
        "mode",
        "user_request",
        "root_framing",
        "root_outcome",
        "domain",
        "domain_ruler",
        "depth_target",
        "width_policy",
        "proof_standard",
        "nodes",
        "edges",
        "next_action",
        "residual_risk",
    ]
    missing = [key for key in required if key not in data]
    require(not missing, f"missing required top-level keys: {', '.join(missing)}")
    require(data["schema_version"] == "1.1", "schema_version must be 1.1")
    require(data["mode"] in {"compact", "focused", "full_tree", "custom"}, "invalid mode")
    require(isinstance(data.get("user_request"), str) and data["user_request"].strip(), "user_request must be non-empty string")
    validate_root_framing(data)
    if "problem_solving" in data:
        validate_problem_solving(data["problem_solving"])
    require(isinstance(data["depth_target"], int), "depth_target must be integer")
    require(2 <= data["depth_target"] <= 12, "depth_target must be 2..12")
    require(isinstance(data["nodes"], list) and data["nodes"], "nodes must be non-empty list")
    require(isinstance(data["edges"], list), "edges must be list")
    require(isinstance(data["proof_standard"], list) and data["proof_standard"], "proof_standard must be non-empty list")
    policy = data["width_policy"]
    require(isinstance(policy, dict), "width_policy must be object")
    require(isinstance(policy.get("min_children_per_parent"), int), "width_policy.min_children_per_parent must be integer")
    require(isinstance(policy.get("max_children_per_parent"), int), "width_policy.max_children_per_parent must be integer")
    require(isinstance(policy.get("max_total_nodes"), int), "width_policy.max_total_nodes must be integer")
    require(1 <= policy["min_children_per_parent"] <= 8, "min_children_per_parent must be 1..8")
    require(1 <= policy["max_children_per_parent"] <= 8, "max_children_per_parent must be 1..8")
    require(
        policy["min_children_per_parent"] <= policy["max_children_per_parent"],
        "min_children_per_parent must be <= max_children_per_parent",
    )
    require(2 <= policy["max_total_nodes"] <= 200, "max_total_nodes must be 2..200")
    if data["mode"] in {"focused", "full_tree", "custom"}:
        require(policy["min_children_per_parent"] >= 5, "focused/full/custom mode requires min_children_per_parent >= 5")
    require(
        policy.get("under_min_strategy") in {"add_unresolved_slots", "ask_user", "mark_deferred"},
        "invalid width_policy.under_min_strategy",
    )
    require(
        policy.get("overflow_strategy") in {"expand_weakest_branches_first", "ask_user", "defer_siblings"},
        "invalid width_policy.overflow_strategy",
    )


def validate_root_framing(data: dict[str, Any]) -> None:
    framing = data.get("root_framing")
    require(isinstance(framing, dict), "root_framing must be object")
    required = [
        "raw_user_ask",
        "selected_root_outcome",
        "root_admission",
        "domain_fit",
        "proof_standard_reason",
        "boundary",
        "misread_risk",
        "clarification_needed",
        "clarification_question",
    ]
    missing = [key for key in required if key not in framing]
    require(not missing, f"root_framing missing keys: {', '.join(missing)}")
    for key in (
        "raw_user_ask",
        "selected_root_outcome",
        "root_admission",
        "domain_fit",
        "proof_standard_reason",
        "boundary",
        "misread_risk",
    ):
        require(text_len(framing.get(key)) >= 1, f"root_framing.{key} must be non-empty string")
    for key in ("root_admission", "domain_fit", "proof_standard_reason", "boundary", "misread_risk"):
        require(text_len(framing.get(key)) >= 8, f"root_framing.{key} needs a concrete explanation")
    require(
        framing["raw_user_ask"].strip() == data["user_request"].strip(),
        "root_framing.raw_user_ask must match user_request",
    )
    require(
        framing["selected_root_outcome"].strip() == data["root_outcome"].strip(),
        "root_framing.selected_root_outcome must match root_outcome",
    )
    require(isinstance(framing.get("clarification_needed"), bool), "root_framing.clarification_needed must be boolean")
    require(isinstance(framing.get("clarification_question"), str), "root_framing.clarification_question must be string")
    if framing["clarification_needed"]:
        require(
            text_len(framing.get("clarification_question")) >= 8,
            "root_framing.clarification_question must be concrete when clarification_needed=true",
        )


def validate_problem_solving(problem: Any) -> None:
    require(isinstance(problem, dict), "problem_solving must be object")
    required = [
        "problem_mode",
        "observed_symptom",
        "desired_normal_result",
        "problem_statement",
        "evidence_seen",
        "likely_missing_child_result",
        "hypothesis_vs_evidence",
        "repair_strategy",
        "verification_check",
    ]
    missing = [key for key in required if key not in problem]
    require(not missing, f"problem_solving missing keys: {', '.join(missing)}")
    extra = sorted(set(problem) - set(required))
    require(not extra, f"problem_solving has unknown keys: {', '.join(extra)}")
    require(isinstance(problem.get("problem_mode"), bool), "problem_solving.problem_mode must be boolean")
    require(isinstance(problem.get("evidence_seen"), list), "problem_solving.evidence_seen must be list")
    for index, item in enumerate(problem.get("evidence_seen", [])):
        require(isinstance(item, str), f"problem_solving.evidence_seen[{index}] must be string")
    if problem["problem_mode"]:
        for key in (
            "observed_symptom",
            "desired_normal_result",
            "problem_statement",
            "likely_missing_child_result",
            "hypothesis_vs_evidence",
            "repair_strategy",
            "verification_check",
        ):
            require(text_len(problem.get(key)) >= 8, f"problem_solving.{key} needs a concrete explanation")
        require(problem["evidence_seen"], "problem_solving.evidence_seen must not be empty when problem_mode=true")


def validate_graph(data: dict[str, Any], strict: bool) -> dict[str, Any]:
    nodes = data["nodes"]
    edges = data["edges"]
    depth_target = data["depth_target"]
    policy = data["width_policy"]
    width_min = policy["min_children_per_parent"]
    width_limit = policy["max_children_per_parent"]
    max_total_nodes = policy["max_total_nodes"]

    require(len(nodes) <= max_total_nodes, f"node count {len(nodes)} exceeds max_total_nodes {max_total_nodes}")

    by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes):
        require(isinstance(node, dict), f"nodes[{index}] must be object")
        node_id = node.get("id")
        require(isinstance(node_id, str) and node_id, f"nodes[{index}] missing id")
        require(node_id not in by_id, f"duplicate node id: {node_id}")
        require(isinstance(node.get("layer"), int), f"node {node_id} layer must be integer")
        require(node["layer"] >= 1, f"node {node_id} layer must be >= 1")
        require(isinstance(node.get("result"), str) and node["result"].strip(), f"node {node_id} missing result")
        require("parent_id" in node, f"node {node_id} missing parent_id")
        require(isinstance(node.get("is_leaf"), bool), f"node {node_id} is_leaf must be boolean")
        require(isinstance(node.get("proof_check"), str) and node["proof_check"].strip(), f"node {node_id} missing proof_check")
        if node["is_leaf"]:
            require(isinstance(node.get("leaf_reason"), str) and node["leaf_reason"].strip(), f"leaf node {node_id} missing leaf_reason")
        by_id[node_id] = node

    roots = [node for node in nodes if node.get("parent_id") is None]
    require(len(roots) == 1, f"must have exactly one root node, got {len(roots)}")
    root = roots[0]
    require(root["layer"] == 1, "root node must be layer 1")
    require(root["result"] == data["root_outcome"], "root_outcome must match root node result")

    children_by_parent: dict[str, list[str]] = defaultdict(list)
    edge_pairs: set[tuple[str, str]] = set()
    for index, edge in enumerate(edges):
        require(isinstance(edge, dict), f"edges[{index}] must be object")
        parent_id = edge.get("parent_id")
        child_id = edge.get("child_id")
        require(parent_id in by_id, f"edge {index} references missing parent {parent_id}")
        require(child_id in by_id, f"edge {index} references missing child {child_id}")
        require(parent_id != child_id, f"edge {index} cannot self-reference")
        pair = (parent_id, child_id)
        require(pair not in edge_pairs, f"duplicate edge {parent_id}->{child_id}")
        edge_pairs.add(pair)
        parent = by_id[parent_id]
        child = by_id[child_id]
        require(child.get("parent_id") == parent_id, f"child {child_id} parent_id does not match edge parent {parent_id}")
        require(child["layer"] == parent["layer"] + 1, f"edge {parent_id}->{child_id} must increment layer by 1")
        edge_kind = edge.get("edge_kind", "causal_child")
        require(edge_kind in {"causal_child", "unresolved_slot"}, f"edge {parent_id}->{child_id} has invalid edge_kind")
        require(text_len(edge.get("parent_needs_child")) >= 8, f"edge {parent_id}->{child_id} missing parent_needs_child")
        require(text_len(edge.get("failure_if_absent")) >= 8, f"edge {parent_id}->{child_id} missing failure_if_absent")
        require(text_len(edge.get("proof_or_action")) >= 1, f"edge {parent_id}->{child_id} missing proof_or_action")
        admission = edge.get("child_admission")
        require(isinstance(admission, dict), f"edge {parent_id}->{child_id} missing child_admission")
        if edge_kind == "unresolved_slot" or child.get("is_unresolved_slot") is True:
            require(child.get("is_unresolved_slot") is True, f"unresolved edge {parent_id}->{child_id} child must set is_unresolved_slot=true")
            require(child.get("is_leaf") is True, f"unresolved edge {parent_id}->{child_id} child must be a leaf")
            unresolved_text = " ".join(str(child.get(key, "")) for key in ("result", "leaf_reason", "proof_check")).lower()
            require(
                "unresolved" in unresolved_text or "想不出来" in unresolved_text,
                f"unresolved edge {parent_id}->{child_id} must say unresolved/想不出来",
            )
        else:
            for key in ("direct_condition", "mechanism_not_label", "proof_named"):
                require(admission.get(key) is True, f"edge {parent_id}->{child_id} child_admission.{key} must be true")
        children_by_parent[parent_id].append(child_id)

    for node_id, node in by_id.items():
        if node["parent_id"] is not None:
            require((node["parent_id"], node_id) in edge_pairs, f"node {node_id} has parent_id but no matching edge")
        child_count = len(children_by_parent[node_id])
        require(child_count <= width_limit, f"node {node_id} has {child_count} children, exceeds width limit {width_limit}")
        if node["layer"] < depth_target and not node["is_leaf"]:
            require(child_count >= width_min, f"non-leaf node {node_id} has {child_count} children, below min {width_min}")
            require(child_count > 0, f"non-leaf node {node_id} at layer {node['layer']} must recurse")
        if node["layer"] < depth_target and node["is_leaf"] and strict:
            leaf_reason = node.get("leaf_reason", "").lower()
            require(
                "directly actionable" in leaf_reason
                or "proof-ready" in leaf_reason
                or "deferred-for-rerun" in leaf_reason
                or "unresolved" in leaf_reason
                or "可直接" in node.get("leaf_reason", "")
                or "叶子" in node.get("leaf_reason", ""),
                f"early leaf {node_id} needs a stronger leaf_reason",
            )

    max_layer = max(node["layer"] for node in nodes)
    require(max_layer >= depth_target, f"max layer {max_layer} is below depth_target {depth_target}")

    require_all_reachable(root["id"], children_by_parent, by_id)
    layer2 = [node for node in nodes if node["layer"] == 2]
    if depth_target >= 4 and strict:
        expanded_layer2 = [
            node for node in layer2 if branch_max_depth(node["id"], children_by_parent, by_id) >= min(depth_target, 4)
        ]
        require(len(expanded_layer2) >= min(2, len(layer2)), "strict mode requires at least two layer-2 branches expanded to depth 4")

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "depth_target": depth_target,
        "max_layer": max_layer,
        "root_id": root["id"],
        "layer_counts": layer_counts(nodes),
    }


def text_len(value: Any) -> int:
    return len(value.strip()) if isinstance(value, str) else 0


def require_all_reachable(root_id: str, children_by_parent: dict[str, list[str]], by_id: dict[str, dict[str, Any]]) -> None:
    seen = {root_id}
    queue: deque[str] = deque([root_id])
    while queue:
        current = queue.popleft()
        for child_id in children_by_parent[current]:
            if child_id not in seen:
                seen.add(child_id)
                queue.append(child_id)
    missing = sorted(set(by_id) - seen)
    require(not missing, f"unreachable nodes: {', '.join(missing)}")


def branch_max_depth(node_id: str, children_by_parent: dict[str, list[str]], by_id: dict[str, dict[str, Any]]) -> int:
    child_ids = children_by_parent.get(node_id, [])
    if not child_ids:
        return by_id[node_id]["layer"]
    return max(branch_max_depth(child_id, children_by_parent, by_id) for child_id in child_ids)


def layer_counts(nodes: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in nodes:
        key = str(node["layer"])
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate outcome-backward process JSON.")
    parser.add_argument("input", type=Path, help="Outcome process JSON path")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Schema path for documentation/reference")
    parser.add_argument("--strict", action="store_true", help="Require stronger early-leaf and branch-depth checks")
    parser.add_argument("--json", action="store_true", help="Print validation summary as JSON")
    args = parser.parse_args(argv)

    try:
        require(args.schema.exists(), f"schema file not found: {args.schema}")
        data = load_json(args.input)
        validate_shape(data)
        summary = validate_graph(data, strict=args.strict)
    except (ValidationError, json.JSONDecodeError) as exc:
        if args.json:
            print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"FAIL {args.input}: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"valid": True, **summary}, ensure_ascii=False, indent=2))
    else:
        print(
            f"PASS {args.input} nodes={summary['node_count']} edges={summary['edge_count']} "
            f"depth={summary['max_layer']}/{summary['depth_target']}"
        )
        print(f"layers: {summary['layer_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
