from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class Intent:
    metric_id: str | None
    dimensions: tuple[str, ...]
    confidence: float
    ambiguities: tuple[str, ...]


METRIC_ALIASES = {
    "net_revenue": ("net revenue", "revenue", "sales"),
    "active_customers": ("active customers", "customers"),
}

DIMENSION_ALIASES = {
    "country": ("country", "market", "region"),
    "channel": ("channel", "sales channel"),
    "product_category": ("product category", "category"),
}


def _contains(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def interpret(question: str) -> Intent:
    text = " ".join(question.casefold().split())

    metric_hits = [
        metric
        for metric, aliases in METRIC_ALIASES.items()
        if any(_contains(text, alias) for alias in aliases)
    ]
    dimension_hits = [
        dim
        for dim, aliases in DIMENSION_ALIASES.items()
        if any(_contains(text, alias) for alias in aliases)
    ]

    ambiguities: list[str] = []
    metric_id = metric_hits[0] if len(metric_hits) == 1 else None
    if not metric_hits:
        ambiguities.append("metric_not_identified")
    elif len(metric_hits) > 1:
        ambiguities.append("multiple_metrics_identified")

    confidence = 0.92 if metric_id else 0.35
    return Intent(metric_id, tuple(sorted(set(dimension_hits))), confidence, tuple(ambiguities))


def build_tool_request(question: str, allowed_metric_ids: Iterable[str]) -> dict:
    intent = interpret(question)
    allowed = set(allowed_metric_ids)

    if intent.metric_id is None:
        return {
            "status": "clarification_required",
            "ambiguities": list(intent.ambiguities),
            "confidence": intent.confidence,
        }
    if intent.metric_id not in allowed:
        return {
            "status": "rejected",
            "reason": "metric_not_governed",
            "metric_id": intent.metric_id,
        }
    return {
        "status": "tool_call_ready",
        "tool": "semantic_query_plan",
        "arguments": {
            "metric_id": intent.metric_id,
            "dimensions": list(intent.dimensions),
        },
        "confidence": intent.confidence,
    }
