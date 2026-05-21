# Quant Desk Anomaly Backend

Backend MVP for an event-driven altcoin anomaly screener.

## Local Setup

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -e .\backend
```

Run one Binance snapshot without Redis/Postgres:

```powershell
.\.venv\Scripts\python -m app.cli binance-snapshot --no-db --no-redis
```

This includes price returns, volume spike, OI and kline-derived CVD.

## Docker Run

```powershell
cd "C:\Users\Денис\Desktop\quant desk"
copy .env.example .env
docker compose up --build
```

API:

```text
http://localhost:8000/api/health
http://localhost:8000/api/metrics/latest
http://localhost:8000/api/sectors/latest
http://localhost:8000/api/events
```

## Workers

Snapshot worker:

```powershell
python -m app.cli run-binance-poll --interval 60
```

Liquidation stream worker:

```powershell
python -m app.cli run-binance-liquidations
```

The liquidation worker listens to Binance Futures `!forceOrder@arr`, stores rolling 15m windows in Redis, and the snapshot worker folds that LIQ data into market/sector metrics.
