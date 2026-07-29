# Quant Desk State

## Current implementation

Frontend:

- terminal-style sector and pair screener;
- global and selected-sector Outlier Radar;
- selected-market Outlook Cockpit;
- integrated AI Risk Analyst with evidence and trace rendering;
- explicit live, cached, unavailable, stale, and fallback states;
- responsive layout that preserves critical columns.

Backend:

- FastAPI application and typed response schemas;
- Binance USD-M REST snapshot pipeline;
- liquidation WebSocket collector;
- sector aggregation and anomaly engine;
- Redis latest state and PostgreSQL history;
- materialized cache fallback;
- bounded OpenAI Responses API workflow with strict structured output;
- deterministic Risk Analyst fallback;
- YAML-based universe, thresholds, and risk playbook.

## Safety boundary

- The agent has two read-only tools.
- Tool requests cannot escape the user-approved symbol or horizon.
- Unknown evidence references and execution language are rejected.
- Every brief requires human review.
- No exchange order API exists.
- Production and staging fail closed around expensive endpoints without an admin key.
- Per-process request budgets protect the localhost demo from accidental abuse.
- Browser output, API error boundaries, security headers, and Docker loopback bindings are hardened.

## Known limitations

- CVD is candle-derived rather than built from an aggregated trade stream.
- The checked-in preview is intentionally stale and demonstrates freshness rejection until a live scan refreshes it.
- Authentication and rate limiting are not implemented.
- Model-backed analysis requires a locally configured OpenAI API key.
