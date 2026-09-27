# Governed Semantic AI Data Agent

A **governed semantic access layer for AI-driven analytics** that prevents unrestricted model access to warehouse structures and exposes only approved business metrics, dimensions, ownership and provenance through a typed FastAPI contract.

![Architecture](https://raw.githubusercontent.com/oleglihvoinen/oleglihvoinen.github.io/main/assets/architecture/semantic-ai-data-agent.png)

## Summary

The design places a formal semantic and governance boundary between natural-language requests and physical data models. AI can interpret user intent and invoke tools, but approved metric definitions, allowed dimensions and ownership rules determine what constitutes a valid analytical request.

## Architecture

Business question → agent/orchestrator → semantic API → approved metric/dimension contract → governed query execution → Snowflake/dbt or Fabric assets → result + provenance.

## Current implementation

- YAML metric contracts for Net Revenue and Active Customers
- FastAPI metric catalogue and lookup endpoints
- Pydantic request validation
- query-plan validation against allowed dimensions
- explicit rejection of unknown metrics and unauthorized dimensions
- provenance returned with approved query plans
- automated API tests
- Docker packaging
- GitHub Actions test workflow

## Governance model

Metric definitions include business description, aggregation, expression, time dimension, allowed dimensions and owner. This makes the semantic layer the authority for business meaning rather than delegating metric interpretation to an LLM.

## Enterprise hardening

A production deployment would add SSO/RBAC, row-level security, Snowflake/Fabric adapters, query compilation, policy enforcement, ambiguity handling, LLM tool calling, caching, audit logging, golden-question evaluation and observability.

## Repository scope

The implementation focuses on semantic contracts, API governance and query-plan validation. Warehouse execution adapters are intentionally separated so the governance boundary can remain stable across Snowflake/dbt or Microsoft Fabric backends.

**Technologies:** Python · FastAPI · REST · Pydantic · YAML semantic contracts · Snowflake/dbt-ready metrics · Microsoft Fabric-ready semantics · LLM grounding · provenance · governance · Docker · CI
