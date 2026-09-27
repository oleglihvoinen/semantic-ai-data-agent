# Governed Semantic AI Data Agent

A reference implementation of a **governed semantic boundary for AI-driven analytics**. Instead of giving an LLM unrestricted access to warehouse tables, the application exposes approved metrics, dimensions, ownership and provenance through a typed FastAPI contract.

## Architecture
Business question → agent/orchestrator → semantic API → approved metric/dimension contract → governed query execution → Snowflake/dbt or Fabric assets → result + provenance.

## Current implementation
- YAML metric contracts for Net Revenue and Active Customers
- FastAPI metric catalogue and lookup endpoints
- query-plan validation against allowed dimensions
- provenance returned with approved plans
- tests for health, unknown metrics and governance rejection
- Docker packaging and GitHub Actions test workflow

## Why it matters
Semantic contracts reduce metric ambiguity, constrain AI tools to approved concepts and create an auditable interface between natural-language questions and physical data models.

## Production evolution
SSO/RBAC, warehouse adapters, SQL/query compilation, row-level security, ambiguity resolution, LLM tool calling, caching, golden-question evaluation, audit logs and observability.

**Technologies:** Python · FastAPI · REST · Pydantic · YAML semantic contracts · Snowflake/dbt-ready metrics · Microsoft Fabric-ready semantics · LLM grounding · provenance · governance · Docker
