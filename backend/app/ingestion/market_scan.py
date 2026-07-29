from __future__ import annotations

import math
from typing import Any

from app.core.config import load_universe
from app.exchanges.binance import BinanceFuturesAdapter

SCAN_LIMITS = {
    "core": 0,
    "expanded": 140,
    "full": 180,
}

SECTOR_KEYWORDS = {
    "Meme": {"DOGE", "SHIB", "PEPE", "FLOKI", "BONK", "WIF", "MEW", "POPCAT", "PENGU", "FARTCOIN", "TURBO", "BRETT", "MOG", "MEME"},
    "AI": {"RENDER", "FET", "TAO", "WLD", "AKT", "NIL", "AI", "ARKM", "KAITO", "GRASS", "PHA", "VANA", "COOKIE"},
    "RWA": {"ONDO", "PENDLE", "CFG", "POLYX", "SKY", "OM", "TOKEN", "TRU"},
    "Layer1": {"BTC", "ETH", "SOL", "ADA", "AVAX", "SUI", "BNB", "TON", "APT", "SEI", "NEAR", "ICP", "DOT", "ATOM", "ALGO"},
    "L2": {"ARB", "OP", "POL", "STRK", "MANTA", "ZK", "ZRO", "STX", "METIS", "BLAST", "SCR"},
    "DeFi": {"AAVE", "CRV", "COMP", "SUSHI", "YFI", "SNX", "LQTY", "GMX", "JTO", "JUP", "UNI", "ENA", "LDO", "MKR"},
    "Oracle": {"LINK", "PYTH", "API3", "BAND", "TRB"},
    "DePIN": {"FIL", "IOTX", "AR", "JASMY", "HNT", "STORJ", "AIOZ"},
    "Gaming": {"IMX", "RONIN", "GALA", "AXS", "SAND", "PIXEL", "PORTAL", "YGG", "GMT", "MAGIC"},
    "Payments": {"XRP", "LTC", "BCH", "XLM", "TRX", "ETC", "XMR", "DASH", "ZEC"},
    "Solana_Eco": {"SOL", "JUP", "PYTH", "W", "MEW", "POPCAT", "PENGU", "FARTCOIN", "GRASS", "JTO"},
    "New_Listings": {"NIL", "WAL", "PARTI", "SHELL", "TUT", "KAITO", "BERA", "IP", "RED", "HYPER", "PUMP", "INIT", "SIGN", "SXT"},
}


def _asset_from_symbol(symbol: str) -> str:
    asset = symbol.removesuffix("USDT")
    return asset.removeprefix("1000")


def _configured_market_maps(universe: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    markets = {
        market["symbol"]: market
        for market in universe.get("markets", [])
        if market.get("exchange") == "binance" and market.get("market_type") == "futures" and market.get("enabled", True)
    }
    sectors = {sector: list(assets) for sector, assets in universe.get("sectors", {}).items()}
    return markets, sectors


def classify_asset(asset: str, configured: dict[str, dict[str, Any]]) -> str:
    for market in configured.values():
        if market.get("asset") == asset and market.get("sector"):
            return market["sector"]
    for sector, assets in SECTOR_KEYWORDS.items():
        if asset in assets:
            return sector
    return "Other"


def _coarse_score(ticker: dict[str, Any], configured: bool) -> float:
    try:
        change = abs(float(ticker.get("priceChangePercent") or 0))
        quote_volume = float(ticker.get("quoteVolume") or 0)
        trade_count = float(ticker.get("count") or 0)
    except (TypeError, ValueError):
        return 0

    liquidity = math.log10(max(quote_volume, 1))
    activity = math.log10(max(trade_count, 1))
    return change * 3.0 + liquidity * 8.0 + activity * 2.0 + (18.0 if configured else 0.0)


async def build_scan_universe(mode: str = "core") -> dict[str, Any]:
    mode = mode if mode in SCAN_LIMITS else "core"
    base_universe = load_universe()
    if mode == "core":
        return base_universe

    configured, base_sectors = _configured_market_maps(base_universe)
    adapter = BinanceFuturesAdapter(timeout=20.0)
    try:
        exchange_info, tickers = await adapter.get_exchange_info(), await adapter.get_24h_ticker()
    except Exception as exc:  # noqa: BLE001 - retain the configured universe when discovery is unavailable
        return {
            **base_universe,
            "scan_mode": mode,
            "scan_unavailable": f"{type(exc).__name__}: {exc}",
            "scan_total_binance_usdt_perps": None,
            "scan_deep_markets": len(configured),
        }
    trading = {
        item["symbol"]
        for item in exchange_info.get("symbols", [])
        if item.get("contractType") == "PERPETUAL"
        and item.get("quoteAsset") == "USDT"
        and item.get("status") == "TRADING"
    }

    ticker_by_symbol = {item["symbol"]: item for item in tickers if item.get("symbol") in trading}
    ranked = sorted(
        ticker_by_symbol.values(),
        key=lambda item: _coarse_score(item, item.get("symbol") in configured),
        reverse=True,
    )

    limit = SCAN_LIMITS[mode]
    selected = {item["symbol"] for item in ranked[:limit]}
    selected.update(symbol for symbol in configured if symbol in trading)

    markets: list[dict[str, Any]] = []
    sectors: dict[str, list[str]] = {sector: list(assets) for sector, assets in base_sectors.items()}
    for symbol in sorted(selected):
        if symbol in configured:
            market = dict(configured[symbol])
        else:
            asset = _asset_from_symbol(symbol)
            market = {
                "exchange": "binance",
                "market_type": "futures",
                "symbol": symbol,
                "asset": asset,
                "quote": "USDT",
                "sector": classify_asset(asset, configured),
                "enabled": True,
            }

        markets.append(market)
        sector_assets = sectors.setdefault(market["sector"], [])
        if market["asset"] not in sector_assets:
            sector_assets.append(market["asset"])

    return {
        **base_universe,
        "scan_mode": mode,
        "scan_total_binance_usdt_perps": len(trading),
        "scan_deep_markets": len(markets),
        "markets": markets,
        "sectors": sectors,
    }
