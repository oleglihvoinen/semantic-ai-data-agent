from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .registry import MetricRegistry

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
