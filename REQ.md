# Quant Desk Requirements

## Goal

Build a practical crypto perpetual-futures screener that highlights the best sectors and pairs for attention.
The app should help the user find early base-breakout and relative-strength situations before they become obvious.

## Product Requirements

- Prefer quality candidates over full-market noise.
- Show sector-level strength and weakness.
- Show pair-level outliers across the whole market.
- Allow pair-level outliers to be filtered by the selected sector.
- Keep `Intrawick` as the main decision horizon.
- Keep `Intraday` as a faster secondary view.
- Use live Binance futures data when available.
- Fall back to cached data when live API data is unavailable.
- Never present old hardcoded demo prices as live market data.

## Signal Ingredients

The screener should rank candidates using confluence from:

- relative strength vs market and sector
- 24H liquidity
- 5M / 24H and 15M volume expansion
- open interest size and OI delta
- OI / market-cap significance
- CVD/TCD confirmation
- multi-day base and consolidation behavior
- breakout behavior from local range
- 4H and 1D EMA support
- orderbook bid/ask wall pressure
- daily FVG proximity or active test
- sector confirmation

## UX Requirements

- The first screen should be the usable terminal, not a landing page.
- The UI should stay dense, scan-friendly and work-focused.
- Data status must be visible: `Live`, `Cached`, `Unavailable`.
- Outlier Radar must clearly indicate whether it is showing `All Market` or `Selected Sector`.
- On narrow screens, critical columns must not disappear silently. At minimum keep sector, signal and OI delta visible.

## Non-Goals

- This is not an entry/exit execution bot.
- This is not a public marketing site.
- Daily FVG is context, not a standalone trigger.
- Current CVD/TCD is a kline-derived proxy until a real trade WebSocket collector is added.

