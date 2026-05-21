from sqlalchemy import JSON, BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Market(Base):
    __tablename__ = "markets"
    __table_args__ = (UniqueConstraint("exchange_id", "market_type", "symbol"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    market_type: Mapped[str] = mapped_column(String, nullable=False)
    quote_asset: Mapped[str] = mapped_column(String, nullable=False)
    min_quote_volume_24h = mapped_column(Numeric)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    exchange = relationship("Exchange")
    asset = relationship("Asset")


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class SectorMember(Base):
    __tablename__ = "sector_members"

    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    weight = mapped_column(Numeric, nullable=False, default=1.0)


class CandleModel(Base):
    __tablename__ = "candles"

    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), primary_key=True)
    timeframe: Mapped[str] = mapped_column(String, primary_key=True)
    open_time = mapped_column(DateTime(timezone=True), primary_key=True)
    close_time = mapped_column(DateTime(timezone=True), nullable=False)
    open = mapped_column(Numeric, nullable=False)
    high = mapped_column(Numeric, nullable=False)
    low = mapped_column(Numeric, nullable=False)
    close = mapped_column(Numeric, nullable=False)
    base_volume = mapped_column(Numeric, nullable=False)
    quote_volume = mapped_column(Numeric, nullable=False)
    trade_count = mapped_column(BigInteger)
    taker_buy_base_volume = mapped_column(Numeric)
    taker_buy_quote_volume = mapped_column(Numeric)
    source_event_time = mapped_column(DateTime(timezone=True))
    inserted_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MarketMetricSnapshot(Base):
    __tablename__ = "market_metric_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), nullable=False)
    ts = mapped_column(DateTime(timezone=True), nullable=False)
    price = mapped_column(Numeric)
    return_5m = mapped_column(Numeric)
    return_15m = mapped_column(Numeric)
    return_1h = mapped_column(Numeric)
    return_24h = mapped_column(Numeric)
    volume_spike_ratio_5m = mapped_column(Numeric)
    quote_volume_5m = mapped_column(Numeric)
    quote_volume_24h = mapped_column(Numeric)
    oi_usd = mapped_column(Numeric)
    oi_change_15m = mapped_column(Numeric)
    funding_rate = mapped_column(Numeric)
    cvd_15m = mapped_column(Numeric)
    liquidations_15m_usd = mapped_column(Numeric)
    long_liquidations_15m_usd = mapped_column(Numeric)
    short_liquidations_15m_usd = mapped_column(Numeric)
    liq_pct_15m = mapped_column(Numeric)
    relative_strength_1h = mapped_column(Numeric)
    data_quality: Mapped[str] = mapped_column(String, nullable=False, default="ok")
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SectorMetricSnapshot(Base):
    __tablename__ = "sector_metric_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), nullable=False)
    ts = mapped_column(DateTime(timezone=True), nullable=False)
    return_5m = mapped_column(Numeric)
    return_1h = mapped_column(Numeric)
    return_24h = mapped_column(Numeric)
    volume_spike_ratio_5m = mapped_column(Numeric)
    quote_volume_5m = mapped_column(Numeric)
    quote_volume_24h = mapped_column(Numeric)
    oi_usd = mapped_column(Numeric)
    oi_change_15m = mapped_column(Numeric)
    cvd_15m = mapped_column(Numeric)
    liquidations_15m_usd = mapped_column(Numeric)
    long_liquidations_15m_usd = mapped_column(Numeric)
    short_liquidations_15m_usd = mapped_column(Numeric)
    liq_pct_15m = mapped_column(Numeric)
    active_member_ratio = mapped_column(Numeric, nullable=False)
    data_quality: Mapped[str] = mapped_column(String, nullable=False, default="ok")
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AnomalyEventModel(Base):
    __tablename__ = "anomaly_events"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    scope: Mapped[str] = mapped_column(String, nullable=False)
    market_id: Mapped[int | None] = mapped_column(ForeignKey("markets.id"))
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"))
    ts = mapped_column(DateTime(timezone=True), nullable=False)
    score = mapped_column(Numeric, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    dedupe_key: Mapped[str] = mapped_column(String, nullable=False)
    formula_inputs = mapped_column(JSON, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AlertDelivery(Base):
    __tablename__ = "alert_deliveries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    anomaly_event_id = mapped_column(UUID(as_uuid=True), ForeignKey("anomaly_events.id"), nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    target: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    error: Mapped[str | None] = mapped_column(Text)
    sent_at = mapped_column(DateTime(timezone=True))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
