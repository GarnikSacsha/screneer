from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field, SecretStr
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
    allowed_origins: list[str] = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]
    allowed_hosts: list[str] = ["127.0.0.1", "localhost", "testserver"]
    admin_api_key: SecretStr | None = None
    expensive_rate_limit_requests: int = Field(default=12, ge=1, le=1000)
    expensive_rate_limit_window_sec: int = Field(default=60, ge=1, le=3600)

    database_url: str = "postgresql+asyncpg://quant:local-development-only@localhost:5432/quantdesk"
    redis_url: str = "redis://localhost:6379/0"

    telegram_bot_token: SecretStr | None = None
    telegram_chat_id: SecretStr | None = None

    risk_agent_enabled: bool = True
    risk_agent_model: str = "gpt-5.6"
    risk_agent_timeout_sec: int = 30
    risk_agent_max_turns: int = 3
    risk_agent_max_snapshot_age_minutes: int = 30
    openai_api_key: SecretStr | None = None

    binance_futures_base_url: str = "https://fapi.binance.com"
    binance_futures_ws_url: str = "wss://fstream.binance.com/ws"
    binance_preview_concurrency: int = 2
    binance_parallel_symbol_requests: bool = False
    binance_request_pause_ms: int = 250
    binance_enable_orderbook: bool = False
    binance_klines_5m_limit: int = 288
    binance_ema_klines_limit: int = 120
    bybit_base_url: str = "https://api.bybit.com"
    okx_base_url: str = "https://www.okx.com"

    config_dir: Path = Field(default_factory=default_config_dir)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "staging"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise TypeError(f"Expected mapping at {path}")

    return data


def load_universe() -> dict[str, Any]:
    return load_yaml_config(get_settings().config_dir / "universe.yaml")


def load_thresholds() -> dict[str, Any]:
    return load_yaml_config(get_settings().config_dir / "thresholds.yaml")


def load_risk_playbook() -> dict[str, Any]:
    return load_yaml_config(get_settings().config_dir / "risk_playbook.yaml")
