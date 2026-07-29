# Quant Desk Requirements

## Product goal

Build a practical perpetual-futures intelligence workspace that helps a human analyst find early sector and pair anomalies, understand the supporting evidence, and identify the risks that could invalidate the observation.

## Core requirements

- Rank quality candidates instead of maximizing market coverage.
- Show sector strength, weakness, participation, and pair-level outliers.
- Support `Intrawick` as the primary horizon and `Intraday` as a faster view.
- Use live Binance USD-M data when available.
- Fall back to a clearly labelled materialized cache when live data is unavailable.
- Never present stale or hard-coded prices as live data.
- Keep critical status, signal, and OI information visible on narrow screens.

## Signal inputs

- relative strength against market and sector;
- 5M, 1H, and 24H price performance;
- 24H liquidity and short-window volume expansion;
- open-interest size, delta, and market-cap significance;
- candle-derived CVD and liquidation pressure;
- multi-day base, breakout, EMA, FVG, and order-book context;
- sector participation and anomaly events.

## AI Risk Analyst requirements

- Use only server-owned snapshot evidence and a local risk playbook.
- Restrict the model to allow-listed, read-only tools.
- Validate tool scope, structured output, evidence references, and prohibited execution language server-side.
- Return only `monitor`, `avoid`, or `needs_context` stances.
- Expose provider, model, latency, token usage, tool calls, safety flags, and fallback reason.
- Require human review and keep execution disabled in every response.
- Use a deterministic fallback when no API key is configured or the provider path fails.
- Treat stale or degraded data as insufficient context.

## Non-goals

- Trade execution, order placement, portfolio allocation, or position sizing.
- Personalized financial advice.
- A public marketing site.
- Treating an FVG or any single metric as a standalone signal.
- Claiming candle-derived CVD is equivalent to aggregated trade flow.
