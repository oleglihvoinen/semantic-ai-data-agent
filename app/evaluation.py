from __future__ import annotations

from dataclasses import dataclass
from .agent import build_tool_request


@dataclass(frozen=True)
class GoldenQuestion:
    question: str
    expected_metric: str | None
    expected_status: str


def evaluate(cases: list[GoldenQuestion], allowed_metric_ids: list[str]) -> dict:
    results = []
    passed = 0
    for case in cases:
        actual = build_tool_request(case.question, allowed_metric_ids)
        actual_metric = actual.get("arguments", {}).get("metric_id")
        ok = actual["status"] == case.expected_status and actual_metric == case.expected_metric
        passed += int(ok)
        results.append({
            "question": case.question,
            "expected_status": case.expected_status,
            "actual_status": actual["status"],
            "expected_metric": case.expected_metric,
            "actual_metric": actual_metric,
            "passed": ok,
        })
    return {
        "total": len(cases),
        "passed": passed,
        "pass_rate": round(passed / len(cases), 4) if cases else 1.0,
        "results": results,
    }
