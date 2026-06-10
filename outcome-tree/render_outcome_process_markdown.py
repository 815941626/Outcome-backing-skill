#!/usr/bin/env python3
"""Render a validated outcome-process JSON as a stable Markdown edge table."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import validate_outcome_process as validator


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def build_paths(data: dict[str, Any]) -> tuple[dict[str, str], dict[str, list[str]]]:
    nodes = data["nodes"]
    node_by_id = {node["id"]: node for node in nodes}
    children_by_parent: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        parent_id = node.get("parent_id")
        if parent_id is not None:
            children_by_parent[parent_id].append(node["id"])

    root = next(node for node in nodes if node.get("parent_id") is None)
    paths = {root["id"]: "R"}

    def visit(parent_id: str) -> None:
        for index, child_id in enumerate(children_by_parent.get(parent_id, []), start=1):
            parent_path = paths[parent_id]
            paths[child_id] = str(index) if parent_path == "R" else f"{parent_path}.{index}"
            visit(child_id)

    visit(root["id"])
    # Keep the linter quiet and make missing node references fail loudly later.
    for node_id in node_by_id:
        paths.setdefault(node_id, "?")
    return paths, children_by_parent


def render_markdown(data: dict[str, Any], source_path: Path) -> str:
    nodes = data["nodes"]
    edges = data["edges"]
    node_by_id = {node["id"]: node for node in nodes}
    edge_by_child = {edge["child_id"]: edge for edge in edges}
    paths, children_by_parent = build_paths(data)
    root = next(node for node in nodes if node.get("parent_id") is None)

    ordered_children: list[str] = []

    def walk(parent_id: str) -> None:
        for child_id in children_by_parent.get(parent_id, []):
            ordered_children.append(child_id)
            walk(child_id)

    walk(root["id"])

    lines: list[str] = []
    lines.append("**Outcome Process Projection**")
    lines.append(f"- Source JSON: `{source_path}`")
    lines.append(f"- Mode: {data['mode']}")
    lines.append(f"- Root outcome: {data['root_outcome']}")
    lines.append(f"- Domain / specialist lens: {data['domain']}")
    lines.append(f"- Domain ruler: {data['domain_ruler']}")
    lines.append(f"- Recursive depth target: {data['depth_target']}")
    lines.append("")
    framing = data.get("root_framing", {})
    lines.append("**Root Framing Gate**")
    lines.append("| Check | Value |")
    lines.append("|---|---|")
    for label, key in (
        ("Raw user ask", "raw_user_ask"),
        ("Selected root outcome", "selected_root_outcome"),
        ("Root admission", "root_admission"),
        ("Domain fit", "domain_fit"),
        ("Proof standard reason", "proof_standard_reason"),
        ("Boundary / non-goals", "boundary"),
        ("Misread risk", "misread_risk"),
        ("Clarification needed", "clarification_needed"),
        ("Clarification question", "clarification_question"),
    ):
        lines.append(f"| {label} | {escape_cell(framing.get(key, ''))} |")
    lines.append("")
    lines.append("**Proof Standard**")
    for item in data["proof_standard"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Recursive Parent-Child Edges**")
    lines.append("| Path | Layer | Parent result | Child result | Why parent needs child | What fails if absent | Proof / action |")
    lines.append("|---|---:|---|---|---|---|---|")
    for child_id in ordered_children:
        child = node_by_id[child_id]
        parent = node_by_id[child["parent_id"]]
        edge = edge_by_child[child_id]
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(paths[child_id]),
                    f"L{parent['layer']} -> L{child['layer']}",
                    escape_cell(parent["result"]),
                    escape_cell(child["result"]),
                    escape_cell(edge["parent_needs_child"]),
                    escape_cell(edge["failure_if_absent"]),
                    escape_cell(edge["proof_or_action"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("**Leaf Nodes**")
    lines.append("| Path | Leaf result | Leaf reason | Proof check |")
    lines.append("|---|---|---|---|")
    for node in nodes:
        if node.get("is_leaf"):
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_cell(paths[node["id"]]),
                        escape_cell(node["result"]),
                        escape_cell(node.get("leaf_reason", "")),
                        escape_cell(node["proof_check"]),
                    ]
                )
                + " |"
            )
    lines.append("")
    lines.append(f"**Weakest current gap:** {data.get('weakest_gap', '')}")
    lines.append(f"**Next action:** {data['next_action']}")
    lines.append(f"**Residual risk:** {data['residual_risk']}")
    return "\n".join(lines)


def escape_cell(value: Any) -> str:
    text = str(value).replace("\n", " ").strip()
    return text.replace("|", "\\|")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render outcome-process JSON to Markdown.")
    parser.add_argument("input", type=Path, help="Outcome process JSON path")
    parser.add_argument("--strict", action="store_true", help="Validate in strict mode before rendering")
    args = parser.parse_args(argv)

    try:
        data = load_json(args.input)
        validator.validate_shape(data)
        validator.validate_graph(data, strict=args.strict)
        print(render_markdown(data, args.input))
    except Exception as exc:
        print(f"FAIL {args.input}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
