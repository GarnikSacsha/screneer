# Quant Desk Agent Handoff

## Product direction

Quant Desk ranks Binance USD-M perpetual-futures sectors and markets using relative strength, liquidity, volume expansion, OI, CVD, liquidation pressure, consolidation, EMA, FVG, order-book, and sector context.

The application should answer:

- Which sectors and markets deserve attention?
- What evidence supports that attention?
- What risks or data gaps invalidate the observation?

It must not place orders or present a single metric as a trade signal.

## Implemented system

- Responsive terminal-style frontend
- Core, Expanded, and Full Market scan modes
- Intrawick and Intraday horizons
- Sector Screener, Outlier Radar, and Outlook Cockpit
- Binance REST snapshot pipeline and liquidation stream collector
- Redis/PostgreSQL persistence and materialized cache
- Bounded AI Risk Analyst with:
  - two allow-listed read-only tools;
  - strict Pydantic structured output;
  - evidence reference and execution-language validation;
  - stale-data rejection;
  - deterministic fallback;
  - run, provider, latency, token, tool, and safety trace.

## Safety invariant

```text
requires_human_review = true
execution_allowed = false
```

There is no exchange order client or execution endpoint.

## Verification baseline

As of 2026-07-29:

- `12 passed`
- Ruff clean
- `node --check app.js` clean
- browser smoke test clean
- risk endpoint verified through the no-key, stale-snapshot fallback path

## Highest-value next work

1. Add a trade WebSocket aggregator to replace candle-derived CVD.
2. Add recorded provider fixtures and API integration tests.
3. Add authentication and rate limiting before any public deployment.
4. Backtest ranking precision using persisted historical snapshots.

## Working conventions

- Talk to the owner in Russian.
- Preserve truthful `Live`, `Cached`, `Stale`, and `Unavailable` states.
- Never commit `.env` or secrets.
- Treat model output as untrusted and preserve the execution boundary.
- Run tests, Ruff, JavaScript syntax validation, and a browser smoke test after relevant changes.
