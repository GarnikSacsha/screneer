def latest_candle(exchange: str, market_type: str, symbol: str, timeframe: str) -> str:
    return f"latest:candle:{exchange}:{market_type}:{symbol}:{timeframe}"


def latest_metrics(exchange: str, market_type: str, symbol: str) -> str:
    return f"latest:metrics:{exchange}:{market_type}:{symbol}"


def latest_sector(sector_code: str) -> str:
    return f"latest:sector:{sector_code}"


def rolling_window(metric: str, market_id: int, timeframe: str) -> str:
    return f"window:{metric}:{market_id}:{timeframe}"


def alert_dedupe(event_type: str, scope: str, identity: str) -> str:
    return f"dedupe:alert:{event_type}:{scope}:{identity}"


def rate_limit(exchange: str, endpoint: str) -> str:
    normalized_endpoint = endpoint.strip("/").replace("/", ":")
    return f"ratelimit:{exchange}:{normalized_endpoint}"


def ws_heartbeat(exchange: str, connection_id: str) -> str:
    return f"ws:heartbeat:{exchange}:{connection_id}"
