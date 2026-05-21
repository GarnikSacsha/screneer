from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def default_config_dir() -> Path:
    cwd_config = Path.cwd() / "config"
    if cwd_config.exists():
        return cwd_config

    repo_config = Path(__file__).resolve().parents[3] / "config"
    if repo_config.exists():
        return repo_config

    return Path("config")


class Settings(BaseSettings):
    app_name: str = "Altcoin Anomaly Screener"
    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://quant:quant@localhost:5432/quantdesk"
    redis_url: str = "redis://localhost:6379/0"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    binance_futures_base_url: str = "https://fapi.binance.com"
    binance_futures_ws_url: str = "wss://fstream.binance.com/ws"
    bybit_base_url: str = "https://api.bybit.com"
    okx_base_url: str = "https://www.okx.com"

    config_dir: Path = Field(default_factory=default_config_dir)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")

    return data


def load_universe() -> dict[str, Any]:
    return load_yaml_config(get_settings().config_dir / "universe.yaml")


def load_thresholds() -> dict[str, Any]:
    return load_yaml_config(get_settings().config_dir / "thresholds.yaml")
