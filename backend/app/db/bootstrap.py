from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.db.models import Asset, Exchange, Market, Sector, SectorMember
from app.db.session import engine


async def create_schema() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def _get_or_create_exchange(session: AsyncSession, code: str, name: str, enabled: bool) -> Exchange:
    result = await session.execute(select(Exchange).where(Exchange.code == code))
    exchange = result.scalar_one_or_none()
    if exchange is None:
        exchange = Exchange(code=code, name=name, enabled=enabled)
        session.add(exchange)
        await session.flush()
    else:
        exchange.name = name
        exchange.enabled = enabled
    return exchange


async def _get_or_create_asset(session: AsyncSession, symbol: str, name: str | None = None) -> Asset:
    result = await session.execute(select(Asset).where(Asset.symbol == symbol))
    asset = result.scalar_one_or_none()
    if asset is None:
        asset = Asset(symbol=symbol, name=name, enabled=True)
        session.add(asset)
        await session.flush()
    elif name and not asset.name:
        asset.name = name
    return asset


async def _get_or_create_sector(session: AsyncSession, code: str, name: str | None = None) -> Sector:
    result = await session.execute(select(Sector).where(Sector.code == code))
    sector = result.scalar_one_or_none()
    if sector is None:
        sector = Sector(code=code, name=name or code, enabled=True)
        session.add(sector)
        await session.flush()
    else:
        sector.name = name or code
        sector.enabled = True
    return sector


async def _get_or_create_market(
    session: AsyncSession,
    exchange: Exchange,
    asset: Asset,
    config: dict[str, Any],
) -> Market:
    result = await session.execute(
        select(Market).where(
            Market.exchange_id == exchange.id,
            Market.market_type == config["market_type"],
            Market.symbol == config["symbol"],
        )
    )
    market = result.scalar_one_or_none()
    if market is None:
        market = Market(
            exchange_id=exchange.id,
            asset_id=asset.id,
            symbol=config["symbol"],
            market_type=config["market_type"],
            quote_asset=config.get("quote", "USDT"),
            enabled=config.get("enabled", True),
        )
        session.add(market)
        await session.flush()
    else:
        market.asset_id = asset.id
        market.quote_asset = config.get("quote", "USDT")
        market.enabled = config.get("enabled", True)
    return market


async def seed_universe(session: AsyncSession, universe: dict[str, Any]) -> None:
    exchanges: dict[str, Exchange] = {}
    for item in universe.get("exchanges", []):
        exchange = await _get_or_create_exchange(
            session,
            code=item["code"],
            name=item.get("name", item["code"]),
            enabled=item.get("enabled", True),
        )
        exchanges[exchange.code] = exchange

    assets: dict[str, Asset] = {}
    for market_config in universe.get("markets", []):
        asset_symbol = market_config["asset"]
        assets[asset_symbol] = await _get_or_create_asset(session, asset_symbol)

    sectors: dict[str, Sector] = {}
    for sector_code, members in universe.get("sectors", {}).items():
        sector = await _get_or_create_sector(session, sector_code)
        sectors[sector_code] = sector

        weight = 1.0 / len(members) if members else 0.0
        for member_symbol in members:
            asset = assets.get(member_symbol) or await _get_or_create_asset(session, member_symbol)
            assets[member_symbol] = asset

            result = await session.execute(
                select(SectorMember).where(
                    SectorMember.sector_id == sector.id,
                    SectorMember.asset_id == asset.id,
                )
            )
            member = result.scalar_one_or_none()
            if member is None:
                session.add(SectorMember(sector_id=sector.id, asset_id=asset.id, weight=weight))
            else:
                member.weight = weight

    for market_config in universe.get("markets", []):
        exchange = exchanges.get(market_config["exchange"])
        if exchange is None:
            continue

        asset = assets[market_config["asset"]]
        await _get_or_create_market(session, exchange, asset, market_config)

    await session.commit()
