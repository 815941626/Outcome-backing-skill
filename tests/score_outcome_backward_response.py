#!/usr/bin/env python3
"""Score an outcome-backward-working response against lightweight eval cases."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_CASES = Path(__file__).with_name("outcome_backward_eval_cases.json")


def load_cases(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def regex_found(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def match_group(patterns: list[str], text: str, mode: str) -> tuple[bool, list[str]]:
    if not patterns:
        return True, []

    matched = [p for p in patterns if regex_found(p, text)]
    if mode == "all":
        missing = [p for p in patterns if p not in matched]
        return len(missing) == 0, missing
    if mode == "any":
        return len(matched) > 0, [] if matched else patterns
    raise ValueError(f"unknown match mode: {mode}")


def score_case(case: dict[str, Any], response: str) -> dict[str, Any]:
    total = 0
    earned = 0
    checks = []

    for item in case.get("required", []):
        points = int(item.get("points", 0))
        total += points

        all_ok, all_missing = match_group(item.get("all", []), response, "all")
        any_ok, any_missing = match_group(item.get("any", []), response, "any")
        passed = all_ok and any_ok
        if passed:
            earned += points

        optional = item.get("optional_any", [])
        optional_hit = [p for p in optional if regex_found(p, response)]

        checks.append(
            {
                "id": item["id"],
                "passed": passed,
                "points": points if passed else 0,
                "max_points": points,
                "description": item.get("description", ""),
                "missing": all_missing + any_missing,
                "optional_hits": optional_hit,
            }
        )

    forbidden_hits = []
    for item in case.get("forbidden", []):
        hits = [p for p in item.get("patterns", []) if regex_found(p, response)]
        if hits:
            forbidden_hits.append(
                {
                    "id": item["id"],
                    "description": item.get("description", ""),
                    "patterns": hits,
                }
            )

    score = round((earned / total) * 100, 1) if total else 0.0
    passed = score >= 80.0 and not forbidden_hits

    return {
        "case_id": case["id"],
        "prompt": case["prompt"],
        "expected_lens": case.get("expected_lens", ""),
        "score": score,
        "earned": earned,
        "total": total,
        "passed": passed,
        "checks": checks,
        "forbidden_hits": forbidden_hits,
    }


def print_report(result: dict[str, Any]) -> None:
    status = "PASS" if result["passed"] else "FAIL"
    print(f"{status} {result['case_id']} score={result['score']} ({result['earned']}/{result['total']})")
    print(f"prompt: {result['prompt']}")
    if result["expected_lens"]:
        print(f"expected_lens: {result['expected_lens']}")
    print()

    for check in result["checks"]:
        mark = "ok" if check["passed"] else "missing"
        print(f"- {mark}: {check['id']} ({check['points']}/{check['max_points']})")
        if check["missing"]:
            print(f"  missing_patterns: {', '.join(check['missing'])}")
        if check["optional_hits"]:
            print(f"  optional_hits: {', '.join(check['optional_hits'])}")

    if result["forbidden_hits"]:
        print()
        print("forbidden_hits:")
        for hit in result["forbidden_hits"]:
            print(f"- {hit['id']}: {', '.join(hit['patterns'])}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="Eval case id")
    parser.add_argument("--response", required=True, type=Path, help="Markdown/text response to score")
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path, help="Eval case JSON")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args(argv)

    data = load_cases(args.cases)
    case = next((c for c in data.get("cases", []) if c.get("id") == args.case), None)
    if not case:
        print(f"unknown case id: {args.case}", file=sys.stderr)
        return 2

    response = args.response.read_text(encoding="utf-8")
    result = score_case(case, response)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
