from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .registry import MetricRegistry
from .agent import build_tool_request
from .evaluation import GoldenQuestion, evaluate

app = FastAPI(title="Governed Semantic Data Agent API", version="1.0.0")
registry = MetricRegistry()

class QueryRequest(BaseModel):
    metric_id: str
    dimensions: list[str] = Field(default_factory=list)
    period: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/metrics")
def metrics():
    return registry.all()

@app.get("/api/v1/metrics/{metric_id}")
def metric(metric_id: str):
    item = registry.get(metric_id)
    if not item:
        raise HTTPException(404, "Unknown or unapproved metric")
    return {"metric": item, "provenance": "semantic/metrics.yml"}

@app.post("/api/v1/query-plan")
def query_plan(req: QueryRequest):
    item = registry.get(req.metric_id)
    if not item:
        raise HTTPException(404, "Unknown or unapproved metric")
    disallowed = [d for d in req.dimensions if d not in item.get("allowed_dimensions", [])]
    if disallowed:
        raise HTTPException(400, detail={"disallowed_dimensions": disallowed})
    return {
        "status": "approved",
        "metric": req.metric_id,
        "dimensions": req.dimensions,
        "period": req.period,
        "semantic_expression": item["expression"],
        "aggregation": item["aggregation"],
        "filter": item.get("filter"),
        "owner": item["owner"],
        "provenance": "semantic/metrics.yml",
    }


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

@app.post("/api/v1/ask")
def ask(req: AskRequest):
    allowed = [m["id"] for m in registry.all()]
    routed = build_tool_request(req.question, allowed)
    if routed["status"] != "tool_call_ready":
        return routed

    arguments = routed["arguments"]
    item = registry.get(arguments["metric_id"])
    disallowed = [
        d for d in arguments["dimensions"]
        if d not in item.get("allowed_dimensions", [])
    ]
    if disallowed:
        return {
            "status": "clarification_required",
            "reason": "dimension_not_approved_for_metric",
            "disallowed_dimensions": disallowed,
        }

    return {
        **routed,
        "semantic_plan": {
            "metric": arguments["metric_id"],
            "dimensions": arguments["dimensions"],
            "expression": item["expression"],
            "aggregation": item["aggregation"],
            "owner": item["owner"],
            "provenance": "semantic/metrics.yml",
        },
        "execution_mode": "plan_only",
    }

@app.get("/api/v1/evaluation")
def evaluation():
    cases = [
        GoldenQuestion("Show net revenue by country", "net_revenue", "tool_call_ready"),
        GoldenQuestion("How many active customers by channel?", "active_customers", "tool_call_ready"),
        GoldenQuestion("What changed yesterday?", None, "clarification_required"),
    ]
    return evaluate(cases, [m["id"] for m in registry.all()])
