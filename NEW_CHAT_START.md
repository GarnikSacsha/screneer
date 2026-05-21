# New Chat Start

Paste this into a fresh chat:

```text
We are continuing my Quant Desk project from the existing workspace.
First read AGENT_HANDOFF.md, then inspect README.md, index.html, app.js, styles.css,
backend/app/ingestion/binance_snapshot.py, backend/app/metrics/engine.py and the backend tests.

Context:
- This is a crypto perpetual-futures screener/terminal, not a marketing site.
- I want it to surface only the best pairs/sectors, especially early base-breakout candidates.
- We already use relative strength, volume, OI, OI/market cap, CVD/TCD, base/consolidation,
  4H/1D EMA zones, orderbook pressure and daily FVG context.
- Recent fixes removed fake demo-price fallback and added D1 FVG detection.

Work style:
- Talk to me in Russian.
- Be proactive: inspect, implement, test, explain clearly.
- Do not overwrite unrelated work.
- Prefer practical usefulness over decorative UI.

Start by summarizing the current architecture, confirm the app runs, and tell me the single best next improvement.
```
