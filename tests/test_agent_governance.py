from app.agent import build_tool_request, interpret
from app.audit import append_audit, verify_chain
from app.evaluation import GoldenQuestion, evaluate


def test_governed_question_routes_to_tool():
    plan = build_tool_request("Show net revenue by country", ["net_revenue", "active_customers"])
    assert plan["status"] == "tool_call_ready"
    assert plan["arguments"]["metric_id"] == "net_revenue"
    assert "country" in plan["arguments"]["dimensions"]


def test_ambiguous_question_requires_clarification():
    plan = build_tool_request("What changed yesterday?", ["net_revenue"])
    assert plan["status"] == "clarification_required"


def test_golden_question_evaluation_is_measurable():
    report = evaluate(
        [
            GoldenQuestion("Revenue by country", "net_revenue", "tool_call_ready"),
            GoldenQuestion("Explain yesterday", None, "clarification_required"),
        ],
        ["net_revenue", "active_customers"],
    )
    assert report["pass_rate"] == 1.0


def test_audit_chain_detects_tampering():
    chain = []
    append_audit(chain, {"metric_id": "net_revenue", "status": "approved"})
    append_audit(chain, {"metric_id": "active_customers", "status": "approved"})
    assert verify_chain(chain) is True
    chain[0]["status"] = "changed"
    assert verify_chain(chain) is False
