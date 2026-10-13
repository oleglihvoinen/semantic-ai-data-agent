# Governed Semantic Layer + AI Data Agent

A governed analytical-AI pattern that combines machine-readable metric contracts with **tool routing, ambiguity handling, evaluation and tamper-evident auditability**.

![Architecture](https://raw.githubusercontent.com/oleglihvoinen/oleglihvoinen.github.io/main/assets/architecture/semantic-ai-data-agent.png)

## Architecture

Business question → governed intent router → semantic policy → approved query plan → Snowflake/dbt or Fabric execution adapter → result + provenance.

The language-model/agent layer is never authoritative for metric meaning.

## Implemented engineering depth

- YAML metric contracts
- FastAPI metric catalogue and query-plan API
- Pydantic validation
- allowed-dimension enforcement
- natural-language metric/dimension router
- explicit clarification when a metric cannot be identified safely
- governed `/api/v1/ask` tool-plan endpoint
- execution remains plan-only in the public repository
- golden-question evaluation harness with measurable pass rate
- evaluation endpoint
- tamper-evident hash-chained audit records
- automated tests for routing, clarification, evaluation and audit integrity
- Docker packaging and CI

## Governance principle

The agent may interpret intent, but it cannot invent a metric, dimension or expression. Approved semantic contracts remain the authority. If intent is ambiguous or a requested dimension is not approved, the system returns a clarification/rejection rather than silently generating SQL.

Warehouse adapters are intentionally separated from the public governance boundary.

**Technologies:** Python · FastAPI · Pydantic · YAML semantic contracts · governed tool calling · evaluation · audit chain · Snowflake/dbt-ready semantics · Microsoft Fabric-ready semantics · Docker · CI
