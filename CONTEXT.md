# Quant Desk Context

## Owner and product

- Preferred conversation language: Russian, casual and precise.
- Quant Desk is an internal crypto perpetual-futures intelligence terminal.
- The objective is to surface a small number of defensible sector and pair anomalies before expansion becomes obvious.
- Intrawick is the primary horizon; intraday is secondary.
- Practical usefulness, truthful data states, and test evidence matter more than decorative UI.

## Current architecture

- Static terminal UI: `index.html`, `styles.css`, `app.js`
- FastAPI application: `backend/app`
- Binance USD-M REST snapshots and liquidation WebSocket ingestion
- Metric, sector aggregation, and anomaly pipeline
- Redis latest state, PostgreSQL history, and materialized JSON fallback
- Bounded AI Risk Analyst under `backend/app/agent`
- Local YAML configuration under `config`

The AI workflow has two read-only tools, strict output validation, human review, no execution capability, and a deterministic fallback.

## Start and verify

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".\backend[dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m ruff check backend
node --check app.js
```

Read `README.md`, `REQ.md`, `STATE.md`, `STATUS.md`, and `docs/architecture/risk-analyst.md` before making architectural changes.
