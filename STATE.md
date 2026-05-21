# Quant Desk State

## Current Working State

Frontend:

- `index.html`, `styles.css`, `app.js`
- Dark terminal-style dashboard
- Sector Screener table with filters and sorting
- Detail panel for selected sector
- Basket constituent table
- Outlier Radar with two scopes:
  - `All Market`
  - `Selected Sector`
- Outlook Cockpit for selected outlier
- Methodology and metric documentation sections

Backend:

- FastAPI app under `backend/`
- Binance USD-M futures preview pipeline
- Live scan universe builder
- Metrics engine for market and sector metrics
- Redis/Postgres support for persisted pipeline mode
- Cached preview fallback via `latest-preview.json`

## Recent Implementation Notes

- Removed misleading demo-price fallback from normal failure flow.
- Added cache fallback for live scan failures.
- Fixed stale scan responses overwriting newer UI state.
- Added daily FVG detection and display in Outlier Radar.
- Added Outlier Radar scope toggle so the radar can be global or tied to the selected sector.
- Adjusted narrow viewport sector rows so `Signal` and `OI delta` remain visible.

## Current Data Behavior

- Core preview usually scans around 98 live pairs from the configured universe.
- Full market scans are slower and noisier.
- Cached preview is legitimate fallback data, but should be visibly marked as cached.
- `latest-preview.json` is included so the UI has a fallback snapshot.

## Known Limitations

- CVD/TCD is still a proxy derived from klines, not a real aggregated trades collector.
- No authentication is implemented for sharing the app outside localhost.
- The repo has a local git history, but GitHub remote push requires user credentials/access.
- Some legacy Russian text in existing docs may have mojibake from earlier encoding issues.

