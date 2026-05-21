# Quant Desk

Internal crypto anomaly screener prototype.

## What Exists Now

- Static UI prototype: `index.html`, `styles.css`, `app.js`
- Metric documentation: `METRICS.md`
- Product/engineering spec: `ANOMALY_SCREENER_TZ.md`
- Backend MVP: `backend/`
- Live universe and thresholds: `config/universe.yaml`, `config/thresholds.yaml`

## Open UI

With the local servers running:

```text
http://127.0.0.1:5500/index.html
```

Or double-click:

```text
open_quant_desk.cmd
```

## Backend MVP

The backend has a Binance Futures snapshot and flow pipeline:

- creates PostgreSQL tables and seeds `config/universe.yaml`
- fetches 5m candles, 24h ticker and open interest
- calculates price performance, volume spike, OI, kline-derived CVD and sector metrics
- collects liquidation events from Binance `!forceOrder@arr` into Redis
- detects anomaly events
- writes latest state to Redis and historical snapshots to PostgreSQL

With Docker installed:

```powershell
cd "C:\Users\Денис\Desktop\quant desk"
copy .env.example .env
docker compose up --build
```

The compose stack starts:

- `backend` on `http://localhost:8000`
- `worker`, which runs a Binance snapshot every 60 seconds
- `liquidation-worker`, which streams force-order events into Redis
- `postgres`
- `redis`

API:

```text
GET http://localhost:8000/api/health
GET http://localhost:8000/api/config/universe
GET http://localhost:8000/api/config/thresholds
GET http://localhost:8000/api/metrics/latest
GET http://localhost:8000/api/sectors/latest
GET http://localhost:8000/api/events
POST http://localhost:8000/api/ingestion/binance/snapshot
POST http://localhost:8000/api/ingestion/binance/preview
```

Local smoke test without Docker:

```powershell
.\.venv\Scripts\python -m app.cli binance-snapshot --no-db --no-redis
```

Run only the liquidation stream collector, if Redis is available:

```powershell
.\.venv\Scripts\python -m app.cli run-binance-liquidations
```

## Next Engineering Step

Add a dedicated CVD trade WebSocket collector and auto-refresh controls in the UI.
