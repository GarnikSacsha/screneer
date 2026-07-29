from __future__ import annotations

import argparse
import asyncio

from app.core.config import load_universe
from app.db.bootstrap import create_schema, seed_universe
from app.db.session import AsyncSessionLocal
from app.ingestion.binance_liquidations import run_binance_liquidation_stream
from app.ingestion.pipeline import run_binance_snapshot


async def init_db() -> None:
    await create_schema()
    async with AsyncSessionLocal() as session:
        await seed_universe(session, load_universe())


async def run_snapshot(args: argparse.Namespace) -> None:
    result = await run_binance_snapshot(
        persist_db=not args.no_db,
        write_redis=not args.no_redis,
        create_tables=not args.no_create_tables,
        read_flow_redis=not args.no_redis,
    )
    print(
        "snapshot ok "
        f"markets={len(result.market_metrics)} "
        f"sectors={len(result.sector_metrics)} "
        f"events={len(result.events)} "
        f"errors={len(result.errors)}"
    )
    for symbol, error in sorted(result.errors.items()):
        print(f"{symbol}: {error}")


async def run_poll(args: argparse.Namespace) -> None:
    first_run = True
    while True:
        try:
            result = await run_binance_snapshot(
                persist_db=not args.no_db,
                write_redis=not args.no_redis,
                create_tables=not args.no_create_tables and first_run,
                read_flow_redis=not args.no_redis,
            )
        except Exception as exc:  # noqa: BLE001 - polling must survive transient provider/storage failures
            print(f"snapshot failed {type(exc).__name__}: {exc}")
        else:
            print(
                "snapshot ok "
                f"markets={len(result.market_metrics)} "
                f"sectors={len(result.sector_metrics)} "
                f"events={len(result.events)} "
                f"errors={len(result.errors)}"
            )
            for symbol, error in sorted(result.errors.items()):
                print(f"{symbol}: {error}")
            first_run = False
        await asyncio.sleep(args.interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quant Desk backend utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Create tables and seed configured universe.")

    snapshot = subparsers.add_parser("binance-snapshot", help="Run one Binance Futures REST snapshot.")
    snapshot.add_argument("--no-db", action="store_true", help="Do not write to PostgreSQL.")
    snapshot.add_argument("--no-redis", action="store_true", help="Do not write latest state to Redis.")
    snapshot.add_argument("--no-create-tables", action="store_true", help="Assume database schema already exists.")

    poll = subparsers.add_parser("run-binance-poll", help="Continuously run Binance REST snapshots.")
    poll.add_argument("--interval", type=int, default=60, help="Polling interval in seconds.")
    poll.add_argument("--no-db", action="store_true", help="Do not write to PostgreSQL.")
    poll.add_argument("--no-redis", action="store_true", help="Do not write latest state to Redis.")
    poll.add_argument("--no-create-tables", action="store_true", help="Assume database schema already exists.")

    liquidation = subparsers.add_parser(
        "run-binance-liquidations",
        help="Collect Binance Futures force-order liquidation events into Redis.",
    )
    liquidation.add_argument("--reconnect-delay", type=float, default=5.0, help="Reconnect delay in seconds.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        asyncio.run(init_db())
        print("database initialized")
        return

    if args.command == "binance-snapshot":
        asyncio.run(run_snapshot(args))
        return

    if args.command == "run-binance-poll":
        asyncio.run(run_poll(args))
        return

    if args.command == "run-binance-liquidations":
        asyncio.run(run_binance_liquidation_stream(reconnect_delay=args.reconnect_delay))


if __name__ == "__main__":
    main()
