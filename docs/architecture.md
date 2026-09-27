# Architecture

The design places a governed semantic contract between natural-language/AI consumers and physical warehouse models.

**Business question → agent/orchestrator → semantic API → approved metric/dimension contract → governed query execution → Snowflake/dbt or Fabric semantic assets → result + provenance.**

The current reference implementation focuses on the contract/API boundary and query-plan validation. Production evolution includes identity-aware permissions, warehouse adapters, query compilation, ambiguity resolution, caching, evaluation sets, audit logs and LLM tool calling.
