# Quant Desk Context

Use this file as the first-stop context for new agents working on this repo.

## Owner

- Preferred language: Russian, casual but precise.
- The owner wants proactive engineering: inspect first, implement, test, then explain plainly.
- This is a practical internal crypto screener/terminal, not a marketing page.
- The product should surface high-quality crypto perpetual futures candidates instead of dumping all market noise.

## Product Idea

Quant Desk is an anomaly screener for Binance USD-M perpetual futures.
It is designed to find sectors and pairs that may be ready for meaningful expansion, especially after consolidation.

The main questions:

- Which sectors are strongest or weakest right now?
- Which pairs deserve attention today?
- Which names are building a base, breaking from consolidation, or becoming outliers?
- Is a move supported by volume, OI, CVD/TCD, orderbook pressure and sector context?
- Is there useful higher-timeframe context such as 4H/1D EMA support or a daily FVG test?

The primary horizon is medium-term / intrawick. Intraday is a secondary view.

## Current Architecture

Frontend:

- Static app in `index.html`, `styles.css`, `app.js`
- Local frontend server usually runs on `http://127.0.0.1:5500/`
- UI modes: `Core`, `Expanded`, `Full Market`
- Horizons: `Intrawick`, `Intraday`
- Sector table, sector detail panel, Outlier Radar and Outlook Cockpit
- Outlier Radar supports `All Market` and `Selected Sector` scopes

Backend:

- FastAPI app in `backend/`
- Local backend usually runs on `http://127.0.0.1:8000/`
- Preview endpoint: `POST /api/ingestion/binance/preview?mode=core`
- Cache fallback endpoint: `GET /api/cache/latest-preview`
- Data sources include Binance futures candles, tickers, open interest, 4H/1D klines and orderbook snapshots

## Important Files

- `README.md` - local run and backend overview
- `REQ.md` - product requirements
- `STATE.md` - current implementation state
- `STATUS.md` - latest status and known verification
- `AGENT_HANDOFF.md` - longer canonical handoff memory
- `ANOMALY_SCREENER_TZ.md` - detailed product/engineering spec
- `METRICS.md` - metric explanations
- `config/universe.yaml` - scan universe
- `config/thresholds.yaml` - anomaly thresholds

## Runbook

Start backend:

```powershell
cd "C:\Users\Денис\Desktop\quant desk\backend"
C:\Users\Денис\Desktop\quant desk\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Start frontend:

```powershell
cd "C:\Users\Денис\Desktop\quant desk"
.\.venv\Scripts\python.exe -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500/
```

Tests:

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests -q
node --check app.js
```

