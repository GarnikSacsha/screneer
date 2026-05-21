# Техническое задание: Altcoin Anomaly Screener

## 1. Цель продукта

Создать event-driven скринер аномалий по альткоинам. Основная задача системы - не показывать красивую таблицу ради таблицы, а находить математически подтвержденные события:

- резкий рост объема;
- ускорение цены;
- изменение open interest;
- секторное лидерство;
- расхождение price / volume / OI / CVD;
- риск squeeze или forced move.

Система должна отвечать на вопрос: "куда сейчас смотреть?", а не "что уже красиво выросло".

## 2. MVP Scope

Первая версия работает только с CEX-данными.

В MVP не включаем on-chain tracker, whale alerts и exchange inflow/outflow. Эти модули добавляются во второй этап после стабилизации CEX anomaly engine.

Причина: on-chain данные дороже, грязнее, имеют задержки, требуют нормализации кошельков и дают больше ложных сигналов без уже работающего market context.

## 3. Технологический стек

### Backend

- Python 3.12+
- FastAPI для HTTP API и WebSocket delivery
- asyncio / aiohttp / websockets для ingestion
- SQLAlchemy 2.x или SQLModel для ORM
- Alembic для миграций
- Pandas/Polars только для backfill/offline research, не для hot path

### Storage

- PostgreSQL 16+ для истории, событий, справочников, audit trail
- Redis 7+ для latest state, rolling windows, deduplication, rate-limit counters

### Delivery

- Telegram Bot API для алертов
- Web UI через существующий frontend или отдельный lightweight dashboard
- REST API для чтения history/events
- WebSocket API для live updates

### Infra

- Docker Compose для local/dev
- systemd или Docker Compose production для MVP
- Prometheus + Grafana опционально для observability
- Sentry или structured logging для ошибок ingestion

## 4. Архитектура

```text
CEX APIs / WebSockets
        |
        v
Data Ingestion Layer
        |
        v
Normalizer
        |
        v
Redis Rolling State <-----> Metric Engine
        |                       |
        v                       v
PostgreSQL History        Anomaly Engine
        |                       |
        +-----------+-----------+
                    |
                    v
              Delivery Layer
        Telegram / Web Dashboard / REST API
```

## 5. Модули

## 5.1 Market Data Ingestion

### Задача

Собирать CEX-данные по заданному universe:

- candles;
- tickers;
- trades;
- open interest;
- funding;
- liquidations, если источник поддерживает.

### Timeframes

Обязательные:

- `1m` - базовый поток;
- `5m` - основной timeframe для anomaly detection;
- `15m` - подтверждение импульса;
- `1h` - локальный тренд;
- `24h` - дневной контекст.

### Источники MVP

#### Binance USD-M Futures

REST:

- `GET /fapi/v1/klines` - candles.
- `GET /fapi/v1/ticker/24hr` - 24h price/volume snapshot.
- `GET /fapi/v1/openInterest` - текущий OI по символу.

WebSocket:

- `<symbol>@kline_<interval>` - live kline update.
- `<symbol>@markPrice` или `<symbol>@markPrice@1s` - mark price + funding.
- `<symbol>@forceOrder` - liquidation order stream.

Документация:

- Binance klines: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
- Binance 24h ticker: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/24hr-Ticker-Price-Change-Statistics
- Binance open interest: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest
- Binance liquidation stream: https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams

#### Bybit V5

REST:

- `GET /v5/market/kline` - candles.
- `GET /v5/market/tickers` - latest price, 24h volume, funding, OI fields.
- `GET /v5/market/open-interest` - historical/current OI by interval.
- `GET /v5/market/recent-trade` - recent public trades for CVD approximation.

WebSocket:

- `allLiquidation.{symbol}` - liquidation stream.

Документация:

- Bybit kline: https://bybit-exchange.github.io/docs/v5/market/kline
- Bybit tickers: https://bybit-exchange.github.io/docs/v5/market/tickers
- Bybit open interest: https://bybit-exchange.github.io/docs/v5/market/open-interest
- Bybit recent trades: https://bybit-exchange.github.io/docs/v5/market/recent-trade
- Bybit all liquidation: https://bybit-exchange.github.io/docs/v5/websocket/public/all-liquidation

#### OKX

REST:

- `GET /api/v5/market/candles` - latest candles.
- `GET /api/v5/market/history-candles` - historical candles.
- `GET /api/v5/market/tickers` - 24h ticker snapshot.
- `GET /api/v5/market/trades` - recent trades.
- `GET /api/v5/public/open-interest` - OI.
- `GET /api/v5/public/funding-rate-history` - funding history.

WebSocket:

- `open-interest` channel - OI updates.
- `funding-rate` channel - funding updates.
- `liquidation-orders` channel - recent liquidation orders.

Документация:

- OKX docs: https://app.okx.com/docs-v5/en/

### Rate Limits

Общие правила:

- WebSocket используется для live data, REST - для backfill и recovery.
- Все REST-вызовы проходят через per-exchange token bucket.
- Для каждого exchange adapter храним лимиты отдельно.
- При HTTP `429` или exchange-specific rate error: exponential backoff + jitter.
- При reconnect WebSocket: backoff `1s -> 2s -> 5s -> 10s -> 30s`, затем держать 30s.

Примеры лимитов, которые надо учитывать:

- Binance `/fapi/v1/klines` имеет weight, зависящий от `limit`.
- Binance `/fapi/v1/ticker/24hr` без `symbol` стоит дороже, чем single-symbol request.
- OKX candles: 40 requests per 2 seconds by IP для `GET /api/v5/market/candles`.
- OKX funding history: 10 requests per 2 seconds by IP + instrument ID.
- Bybit V5 требует учитывать category и endpoint-level limits; лимиты держать конфигом, не хардкодить в коде.

## 5.2 Normalizer

### Задача

Привести данные разных бирж к единому формату.

### Canonical market key

```text
exchange:market_type:symbol
```

Примеры:

```text
binance:futures:BTCUSDT
bybit:linear:BTCUSDT
okx:swap:BTC-USDT-SWAP
```

### Normalized candle

```json
{
  "exchange": "binance",
  "market_type": "futures",
  "symbol": "SOLUSDT",
  "timeframe": "5m",
  "open_time": "2026-05-03T12:00:00Z",
  "close_time": "2026-05-03T12:04:59.999Z",
  "open": 142.1,
  "high": 144.8,
  "low": 141.9,
  "close": 144.2,
  "base_volume": 922340.12,
  "quote_volume": 132940000.0,
  "trade_count": 18210,
  "is_closed": true,
  "source_event_time": "2026-05-03T12:05:00.120Z"
}
```

## 5.3 Metric Engine

### Задача

Считать метрики по каждому market и по сектору.

### Базовые формулы

#### Price return

```text
return_pct(tf) = (close_now / close_tf_ago - 1) * 100
```

#### Volume spike ratio

Используем rolling median, а не mean, чтобы одиночные выбросы не ломали базу.

```text
volume_spike_ratio_5m =
  current_5m_quote_volume / median(last_288_closed_5m_quote_volumes)
```

`288` свечей по `5m` = 24 часа.

#### Open Interest change

```text
oi_change_pct(tf) = (oi_now - oi_tf_ago) / oi_tf_ago * 100
```

#### CVD

```text
cvd_tf = sum(taker_buy_quote_volume) - sum(taker_sell_quote_volume)
```

Если источник отдает только trade side:

```text
trade_delta = price * size * side_sign
side_sign = +1 for taker buy, -1 for taker sell
```

#### Sector return

```text
sector_return_tf = avg(member_return_tf)
```

Equal-weighted, без market-cap весов.

#### Relative strength

```text
relative_strength_tf = asset_return_tf - sector_return_tf
```

#### LIQ %

Для MVP:

```text
liq_pct_15m = liquidations_quote_15m / quote_volume_15m * 100
```

Для derivatives mode:

```text
liq_pct_oi_15m = liquidations_quote_15m / open_interest_quote_now * 100
```

### Минимальные thresholds MVP

Хранить в YAML/DB, не хардкодить.

```yaml
volume_spike:
  ratio_min: 2.0
  min_quote_volume_5m: 1000000

oi_expansion:
  change_15m_min_pct: 3.0
  min_oi_usd: 5000000

price_breakout:
  return_15m_min_pct: 3.0
  volume_spike_ratio_min: 1.8

squeeze_risk:
  liq_pct_15m_min: 2.0
  long_short_skew_min: 0.65

sector_leader:
  top_n: 3
  return_1h_min_pct: 2.0

lagging_asset:
  sector_return_1h_min_pct: 2.0
  asset_underperformance_min_pct: 1.5
```

## 5.4 Anomaly Engine

### Задача

Генерировать события только по математическим условиям.

### Event types

#### Volume Spike

```text
volume_spike_ratio_5m >= 2.0
AND quote_volume_5m >= min_quote_volume_5m
AND market_status = active
```

#### OI Expansion

```text
oi_change_15m_pct >= 3.0
AND open_interest_usd >= min_oi_usd
```

#### Price Breakout

```text
return_15m_pct >= 3.0
AND volume_spike_ratio_5m >= 1.8
```

#### Squeeze Risk

```text
liq_pct_15m >= 2.0
AND max(long_liq_share, short_liq_share) >= 0.65
```

#### Sector Leader

```text
sector_return_1h ranks in top 3
AND sector_return_1h >= 2.0
```

#### Lagging Asset

```text
sector_return_1h >= 2.0
AND asset_return_1h < sector_return_1h - 1.5
AND asset_volume_spike_ratio_5m >= 1.2
```

#### Absorption Candidate

```text
cvd_15m < 0
AND abs(return_15m_pct) <= 0.5
AND oi_change_15m_pct > 0
```

### Anomaly score

Не использовать subjective score. Только формула:

```text
score =
  min(volume_spike_ratio_5m / 5.0, 1.0) * 25
  + min(abs(return_15m_pct) / 10.0, 1.0) * 20
  + min(abs(oi_change_15m_pct) / 10.0, 1.0) * 20
  + min(liq_pct_15m / 5.0, 1.0) * 20
  + min(abs(relative_strength_1h) / 5.0, 1.0) * 15
```

Итоговый score: `0..100`.

## 5.5 Sector Analysis

### MVP sectors

```yaml
AI:
  - RNDR
  - FET
  - AGIX
  - OCEAN
  - AKT

RWA:
  - ONDO
  - OM
  - PENDLE
  - CFG
  - POLYX

Gaming:
  - IMX
  - RON
  - GALA
  - AXS
  - SAND

L2:
  - ARB
  - OP
  - MATIC
  - STRK
  - MANTA
```

### Sector metrics

```text
sector_return_5m = avg(member_return_5m)
sector_return_1h = avg(member_return_1h)
sector_return_24h = avg(member_return_24h)
sector_volume_spike = median(member_volume_spike_ratio_5m)
sector_oi_change = avg(member_oi_change_15m)
sector_cvd = sum(member_cvd_15m)
```

### Missing members

Если у сектора меньше 60% active members, сектор не участвует в ranking.

```text
active_member_ratio = active_members / configured_members
```

## 6. Storage

## 6.1 PostgreSQL schema

### `exchanges`

```sql
CREATE TABLE exchanges (
  id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### `assets`

```sql
CREATE TABLE assets (
  id SERIAL PRIMARY KEY,
  symbol TEXT UNIQUE NOT NULL,
  name TEXT,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### `markets`

```sql
CREATE TABLE markets (
  id BIGSERIAL PRIMARY KEY,
  exchange_id INT NOT NULL REFERENCES exchanges(id),
  asset_id INT NOT NULL REFERENCES assets(id),
  symbol TEXT NOT NULL,
  market_type TEXT NOT NULL,
  quote_asset TEXT NOT NULL,
  min_quote_volume_24h NUMERIC,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(exchange_id, market_type, symbol)
);
```

### `sectors`

```sql
CREATE TABLE sectors (
  id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE
);
```

### `sector_members`

```sql
CREATE TABLE sector_members (
  sector_id INT NOT NULL REFERENCES sectors(id),
  asset_id INT NOT NULL REFERENCES assets(id),
  weight NUMERIC NOT NULL DEFAULT 1.0,
  PRIMARY KEY (sector_id, asset_id)
);
```

### `candles`

```sql
CREATE TABLE candles (
  market_id BIGINT NOT NULL REFERENCES markets(id),
  timeframe TEXT NOT NULL,
  open_time TIMESTAMPTZ NOT NULL,
  close_time TIMESTAMPTZ NOT NULL,
  open NUMERIC NOT NULL,
  high NUMERIC NOT NULL,
  low NUMERIC NOT NULL,
  close NUMERIC NOT NULL,
  base_volume NUMERIC NOT NULL,
  quote_volume NUMERIC NOT NULL,
  trade_count BIGINT,
  source_event_time TIMESTAMPTZ,
  inserted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (market_id, timeframe, open_time)
);
```

### `market_metric_snapshots`

```sql
CREATE TABLE market_metric_snapshots (
  id BIGSERIAL PRIMARY KEY,
  market_id BIGINT NOT NULL REFERENCES markets(id),
  ts TIMESTAMPTZ NOT NULL,
  return_5m NUMERIC,
  return_15m NUMERIC,
  return_1h NUMERIC,
  return_24h NUMERIC,
  volume_spike_ratio_5m NUMERIC,
  oi_usd NUMERIC,
  oi_change_15m NUMERIC,
  funding_rate NUMERIC,
  cvd_15m NUMERIC,
  liquidations_15m_usd NUMERIC,
  liq_pct_15m NUMERIC,
  relative_strength_1h NUMERIC,
  data_quality TEXT NOT NULL DEFAULT 'ok',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_market_metric_snapshots_market_ts
ON market_metric_snapshots (market_id, ts DESC);
```

### `sector_metric_snapshots`

```sql
CREATE TABLE sector_metric_snapshots (
  id BIGSERIAL PRIMARY KEY,
  sector_id INT NOT NULL REFERENCES sectors(id),
  ts TIMESTAMPTZ NOT NULL,
  return_5m NUMERIC,
  return_1h NUMERIC,
  return_24h NUMERIC,
  volume_spike_ratio_5m NUMERIC,
  oi_change_15m NUMERIC,
  cvd_15m NUMERIC,
  active_member_ratio NUMERIC NOT NULL,
  data_quality TEXT NOT NULL DEFAULT 'ok',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### `anomaly_events`

```sql
CREATE TABLE anomaly_events (
  id UUID PRIMARY KEY,
  event_type TEXT NOT NULL,
  scope TEXT NOT NULL,
  market_id BIGINT REFERENCES markets(id),
  sector_id INT REFERENCES sectors(id),
  ts TIMESTAMPTZ NOT NULL,
  score NUMERIC NOT NULL,
  severity TEXT NOT NULL,
  dedupe_key TEXT NOT NULL,
  formula_inputs JSONB NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_anomaly_events_ts ON anomaly_events (ts DESC);
CREATE INDEX idx_anomaly_events_type_ts ON anomaly_events (event_type, ts DESC);
CREATE UNIQUE INDEX idx_anomaly_events_dedupe_recent
ON anomaly_events (dedupe_key, ts);
```

### `alert_deliveries`

```sql
CREATE TABLE alert_deliveries (
  id BIGSERIAL PRIMARY KEY,
  anomaly_event_id UUID NOT NULL REFERENCES anomaly_events(id),
  channel TEXT NOT NULL,
  target TEXT NOT NULL,
  status TEXT NOT NULL,
  error TEXT,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 6.2 Redis keys

```text
latest:candle:{exchange}:{market_type}:{symbol}:{tf}
latest:metrics:{exchange}:{market_type}:{symbol}
latest:sector:{sector_code}

window:volume:{market_id}:5m
window:price:{market_id}:1m
window:oi:{market_id}:5m
window:cvd:{market_id}:1m
window:liq:{market_id}:1m

dedupe:alert:{event_type}:{scope}:{id}
ratelimit:{exchange}:{endpoint}
ws:heartbeat:{exchange}:{connection_id}
```

TTL:

- latest state: 10 minutes;
- rolling windows: 48 hours;
- dedupe keys: 15-60 minutes depending on event type;
- rate-limit keys: according to exchange interval.

## 7. Missing Data Strategy

### Market status

```text
active: all required feeds fresh
degraded: one non-critical feed missing
stale: no candle/ticker update for > 2 intervals
disabled: manually disabled or delisted
```

### Rules

- Если нет закрытой свечи для timeframe, метрика по этому timeframe не считается.
- Если `lookback < min_required_points`, anomaly event не генерируется.
- Если OI отсутствует, события `OI Expansion`, `Absorption Candidate`, `Squeeze Risk` не генерируются.
- Если liquidation stream отсутствует, `liq_pct` ставится `null`, а не `0`.
- `null` не заменять нулем в формулах.
- Для dashboard stale markets показывать отдельным статусом.

### Minimum data requirements

```yaml
volume_spike:
  min_closed_5m_candles: 144

return_24h:
  min_closed_1h_candles: 24

oi_change:
  min_oi_points: 2

sector_ranking:
  min_active_member_ratio: 0.6
```

## 8. Alerting

### Telegram message rules

- Не отправлять больше одного одинакового события по `dedupe_key` за TTL.
- Severity:
  - `info`: score < 50
  - `medium`: 50 <= score < 70
  - `high`: 70 <= score < 85
  - `critical`: score >= 85

### Example anomaly event JSON

```json
{
  "event_id": "8e2c39d4-72d7-4fb7-bfa0-9c7e9f6e1d82",
  "event_type": "VOLUME_SPIKE",
  "scope": "market",
  "exchange": "binance",
  "market_type": "futures",
  "symbol": "SOLUSDT",
  "asset": "SOL",
  "sector": "Layer1",
  "timeframe": "5m",
  "ts": "2026-05-03T12:05:00Z",
  "score": 78.4,
  "severity": "high",
  "formula_inputs": {
    "quote_volume_5m": 132940000.0,
    "median_quote_volume_5m_24h": 42100000.0,
    "volume_spike_ratio_5m": 3.16,
    "return_15m_pct": 2.7,
    "oi_change_15m_pct": 3.4
  },
  "message": "SOLUSDT volume spike: 3.16x vs 24h median, OI +3.40% in 15m."
}
```

### Example Telegram payload

```json
{
  "chat_id": "-1001234567890",
  "parse_mode": "HTML",
  "text": "<b>HIGH: VOLUME_SPIKE</b>\nSOLUSDT Binance Futures\nVolume: 3.16x vs 24h median\n15m return: +2.70%\nOI 15m: +3.40%\nScore: 78.4"
}
```

### Example sector event

```json
{
  "event_id": "2a8c42df-3f0d-4a0e-9fc0-e225ddc69de1",
  "event_type": "SECTOR_LEADER",
  "scope": "sector",
  "sector": "AI",
  "timeframe": "1h",
  "ts": "2026-05-03T12:00:00Z",
  "score": 71.2,
  "severity": "high",
  "formula_inputs": {
    "sector_return_1h": 4.82,
    "market_rank": 1,
    "active_member_ratio": 0.83,
    "members": ["RNDR", "FET", "AGIX", "OCEAN", "AKT"]
  },
  "message": "AI sector is #1 by 1h return: +4.82%, active members 83%."
}
```

## 9. API Backend для Dashboard

### REST

```text
GET /api/markets
GET /api/sectors
GET /api/metrics/latest
GET /api/events?event_type=&severity=&sector=&limit=
GET /api/events/{event_id}
GET /api/health
```

### WebSocket

```text
WS /ws/live
```

Message types:

```json
{
  "type": "metric_update",
  "payload": {}
}
```

```json
{
  "type": "anomaly_event",
  "payload": {}
}
```

## 10. Конфигурация

### `config/universe.yaml`

```yaml
exchanges:
  - binance
  - bybit
  - okx

markets:
  - exchange: binance
    market_type: futures
    symbol: SOLUSDT
    asset: SOL
    quote: USDT
    enabled: true

sectors:
  AI:
    - RNDR
    - FET
    - AGIX
    - OCEAN
    - AKT
```

### `config/thresholds.yaml`

```yaml
global:
  min_quote_volume_24h: 10000000
  stale_intervals_allowed: 2

events:
  volume_spike:
    ratio_min: 2.0
    dedupe_ttl_sec: 900
  oi_expansion:
    change_15m_min_pct: 3.0
    dedupe_ttl_sec: 900
  sector_leader:
    return_1h_min_pct: 2.0
    dedupe_ttl_sec: 1800
```

## 11. Acceptance Criteria

### Data ingestion

- Система получает и нормализует candles `1m`, `5m`, `15m`, `1h` минимум по 50 рынкам.
- При разрыве WebSocket система восстанавливает соединение и делает REST backfill пропущенных candles.
- REST requests не превышают configured rate limits.
- Все входящие raw/normalized ошибки логируются structured JSON.

### Metric engine

- `volume_spike_ratio_5m` считается через rolling median за 24h.
- `return_5m`, `return_1h`, `return_24h` не считаются при недостаточном lookback.
- `oi_change_15m` не считается, если нет двух валидных OI points.
- `null` значения не заменяются нулями.

### Anomaly engine

- События генерируются только при выполнении формальных условий.
- Каждое событие содержит `formula_inputs`.
- Дубликаты подавляются через Redis dedupe key.
- Для каждого event type есть unit tests на positive/negative cases.

### Storage

- PostgreSQL хранит candles, metric snapshots, anomaly events, alert deliveries.
- Redis хранит latest state и rolling windows.
- Повторная вставка одной свечи не создает дубль благодаря primary key.

### Dashboard / Alerts

- Telegram alert содержит event type, symbol/sector, score, severity и ключевые inputs.
- Dashboard показывает latest metrics и последние anomaly events.
- Stale markets визуально отделены и не участвуют в ranking/scoring.

### Performance MVP

- 50 markets, 1m/5m live updates.
- Задержка от закрытия 1m candle до расчета metrics: не более 3 секунд.
- Задержка от anomaly detection до Telegram alert: не более 5 секунд.
- Сервис должен продолжать работу при падении одного exchange adapter.

## 12. Этапы разработки

### Stage 1: Foundation

- Docker Compose: Postgres + Redis + backend.
- Config loading.
- Exchange adapter interface.
- Binance futures ingestion.
- PostgreSQL migrations.

### Stage 2: Metrics

- Rolling windows в Redis.
- Metric engine.
- Market snapshots.
- Unit tests formulas.

### Stage 3: Anomalies

- Event rules.
- Dedupe.
- PostgreSQL event persistence.
- Telegram delivery.

### Stage 4: Dashboard API

- REST latest metrics.
- REST events.
- WebSocket live stream.
- Подключение текущего frontend prototype к API.

### Stage 5: Multi-exchange

- Bybit adapter.
- OKX adapter.
- Symbol mapping.
- Cross-exchange aggregation.

### Stage 6: On-chain Phase 2

- Whale alerts.
- Exchange inflow/outflow.
- Address labeling.
- Chain-specific adapters.

## 13. Что не входит в MVP

- Автоматические торговые действия.
- Predictive ML model.
- On-chain whale tracker.
- Portfolio management.
- PnL tracking.
- User auth / multi-tenant roles.

## 14. Важные замечания

- Liquidation streams у бирж могут быть неполными или агрегированными. В UI и документации обязательно помечать, что `liq_pct` основан на доступном feed, а не гарантированно на полном рынке.
- Сравнение между биржами требует нормализации contract size, quote currency и symbol mapping.
- Секторные метрики должны исключать stale members.
- Все thresholds должны быть конфигурируемыми.
