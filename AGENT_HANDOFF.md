# Quant Desk Agent Handoff

Use this file when continuing the project in a new AI-agent chat or on another account.
It is the canonical project memory for the next agent.

## Owner Context

- Preferred language: Russian, casual but precise.
- The owner is building a practical crypto screener/terminal, not a landing page.
- The core idea is to catch names before or near meaningful expansion, especially after consolidation:
  unusual volume, OI expansion, CVD/TCD confirmation, relative strength, sector confirmation,
  base breakout behavior, EMA support, orderbook pressure and now daily FVG context.
- The owner likes proactive work: inspect first, implement, test, then explain plainly.

## Product Goal

Quant Desk is an internal crypto anomaly screener for perpetual futures.
It should help answer:

- Which sectors are strongest or weakest now?
- Which pairs deserve attention today instead of showing all market noise?
- Which names are building a base, breaking from consolidation, or becoming outliers?
- Is the move supported by volume, OI, CVD/TCD, orderbook and broader sector context?
- Is there nearby higher-timeframe structure such as 4H/1D EMA support or a daily FVG test?

The product direction is medium-term / intrawick first, with intraday as a secondary view.

## Current Working State

Frontend:

- Static dashboard in `index.html`, `styles.css`, `app.js`
- Dark Runway-inspired visual redesign already applied
- Modes: `Core`, `Expanded`, `Full Market`
- Horizons: `Intrawick`, `Intraday`
- Sector screener table
- Detail panel with setup read
- Outlier Radar
- Outlook cockpit / confluence panel
- Structured methodology block at the bottom of the page
- Data-state labels: `Live`, `Cached`, `Unavailable`

Backend:

- FastAPI app in `backend/`
- Binance USD-M Futures preview pipeline
- 5m candles, 24h ticker, open interest, 4H and 1D klines, orderbook snapshots
- kline-derived CVD/TCD proxy
- base/consolidation metrics
- 4H/1D EMA metrics
- OI / market-cap comparison
- orderbook bid/ask wall metrics
- cached preview endpoint: `GET /api/cache/latest-preview`
- daily FVG metrics added from 1D candles:
  - `daily_fvg_side`
  - `daily_fvg_low`
  - `daily_fvg_high`
  - `daily_fvg_age_days`
  - `daily_fvg_distance_pct`
  - `daily_fvg_test`

Recent important fixes:

- Removed misleading demo-price fallback from normal app failure flow.
  If API data is unavailable, UI now says unavailable instead of showing stale fake market prices.
- Fixed old incorrect constituent prices such as DOGE and ETH demo values leaking into the UI.
- Added cache fallback and fixed BOM reading for `latest-preview.json`.
- Fixed logic where stale scan responses could overwrite newer UI state.
- Added daily FVG detection and display in `Outlier Radar` as `D1 FVG`.
- Current UI exposes daily FVG like:
  - `Bull test`
  - `Bear test`
  - `Bull +x%`
  - `Bear -x%`

## How The Screener Thinks

The screener should not dump every available pair at the user.
It should prefer pairs that satisfy more of the following:

- relative strength vs market and sector
- meaningful 24H liquidity
- local 5M / 24H volume expansion
- OI growth
- OI / market-cap significance
- positive or negative CVD/TCD confirmation
- multi-day base / consolidation behavior
- breakout behavior from local range
- 4H and 1D EMA support
- orderbook imbalance / wall behavior
- daily FVG proximity or active test
- sector confirmation

The owner is especially interested in early situations like ONDO and NIL:
names that spend time in a base, then break cleanly with supporting metrics before the move becomes obvious.

## Key Files

Root:

- `index.html`
- `styles.css`
- `app.js`
- `README.md`
- `METRICS.md`
- `ANOMALY_SCREENER_TZ.md`
- `latest-preview.json`
- `config/universe.yaml`
- `config/thresholds.yaml`

Backend:

- `backend/app/api/routes.py`
- `backend/app/ingestion/binance_snapshot.py`
- `backend/app/ingestion/pipeline.py`
- `backend/app/metrics/engine.py`
- `backend/app/domain/entities.py`
- `backend/app/schemas.py`
- `backend/app/state/redis_store.py`
- `backend/tests/test_metrics_engine.py`
- `backend/tests/test_anomaly_rules.py`
- `backend/tests/test_binance_snapshot.py`

## Local Runbook

Start frontend:

```powershell
cd "C:\Users\Денис\Desktop\quant desk"
.\.venv\Scripts\python.exe -m http.server 5500
```

Start backend:

```powershell
cd "C:\Users\Денис\Desktop\quant desk\backend"
C:\Users\Денис\Desktop\quant desk\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open UI:

```text
http://127.0.0.1:5500/
```

Health:

```text
http://127.0.0.1:8000/api/health
```

Tests:

```powershell
cd "C:\Users\Денис\Desktop\quant desk"
.\.venv\Scripts\python.exe -m pytest backend\tests -q
node --check app.js
```

Latest known green result:

- `7 passed`
- `node --check app.js` OK

## Important Behavioral Notes

- The app may fall back to cached data when Binance rate-limits or a live scan fails.
- Cached data is legitimate fallback; old hardcoded demo market values should not be used as if live.
- Full market scans can be slower and noisy; the product direction is to surface the best candidates, not all 529 pairs by default.
- Sector rows and detail panel can disagree if one label describes directional signal and another describes flow regime.
  This was partly clarified in UI already, but new work should preserve clear language.
- Daily FVG is context, not an entry trigger by itself.

## Likely Next Steps

1. Add a dedicated trade WebSocket collector for real CVD/TCD instead of kline proxy.
2. Improve docs and UI copy around daily FVG, base logic and score composition.
3. Add persistent historical snapshots for backtesting candidate quality.
4. Add a quality ranking for “best pairs today” so junk is hidden by default.
5. Improve orderbook-pressure logic across falling/rising price conditions.
6. Add richer regression tests for UI payload assumptions and cached/live transitions.
7. Initialize git if the owner wants reliable version history.

## New Chat Starter Prompt

Paste this into a new chat:

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

## Transfer Checklist

When moving to another account or machine, include:

- project source folder
- `AGENT_HANDOFF.md`
- `README.md`
- `ANOMALY_SCREENER_TZ.md`
- `METRICS.md`
- `backend/`
- `config/`
- `latest-preview.json`
- `.env.example`
- `docker-compose.yml`

Do not include:

- `.venv/`
- real `.env` secrets
- generated caches such as `__pycache__/`
