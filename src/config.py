# src/config.py
"""Application configuration models.

This module provides a small ``Settings`` class used throughout the
application.  The original project relied on the third-party
``pydantic-settings`` package for this purpose.  The execution environment
for the kata does not include that dependency, so a very small shim version
of the library is provided under ``src/pydantic_settings``.  The shim only
implements the features we need here (basic attribute handling) but keeps the
same API so the rest of the code does not need to change.
"""
from collections.abc import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the trading application.

    Values are loaded from environment variables when present and otherwise
    fall back to the defaults declared below.

    Example:
        >>> from config import Settings
        >>> settings = Settings()
        >>> settings.symbol_list
        ['AAPL', 'MSFT', 'SPY']
    """

    env: str = "dev"  # environment name; defaults to 'dev'
    alpaca_key_id: str | None = None  # Alpaca API key ID; defaults to None
    alpaca_secret_key: str | None = None  # Alpaca API secret key; defaults to None
    alpaca_base_url: str = "https://paper-api.alpaca.markets"  # Alpaca API base URL (paper)
    symbols: Sequence[str] | str = ("AAPL", "MSFT", "SPY")  # default asset symbols to trade
    schedule_cron: str = "*/5 * * * *"  # cron schedule for main job; every five minutes

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )  # load variables from .env with case-insensitive keys

    @property
    def symbol_list(self) -> list[str]:
        """Return the configured symbols as a list of non-empty tickers."""

        value = self.symbols
        if isinstance(value, str):
            cleaned = [item.strip().strip("'\"") for item in value.split(",")]
            return [item for item in cleaned if item]
        if isinstance(value, Sequence):
            return [str(item) for item in value if str(item)]
        return [str(value)] if value else []
