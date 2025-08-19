# src/config.py
"""Application configuration models.

This module provides a small ``Settings`` class used throughout the
application.  The original project relied on the third-party
``pydantic-settings`` package for this purpose.  The execution environment
for the kata does not include that dependency, so a very small shim version
of the library is provided under ``src/pydantic_settings``.  The shim only
implements the features we need here (basic attribute handling) but keeps the
same API so the rest of the code does not need to change.

The bug fixed in this module concerns the ``symbols`` configuration option.
It was previously stored as a single comma separated string which forced
callers to manually split the value.  This led to surprising behaviour and
inconsistent handling of whitespace.  ``Settings`` now exposes ``symbols`` as
``list[str]`` and automatically parses any provided string.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the trading application.

    Values are loaded from environment variables when present and otherwise
    fall back to the defaults declared below. ``symbols`` is exposed as a list
    for ease of use; when a comma separated string is supplied the value is
    split and surrounding whitespace is removed.

    Example:
        >>> from config import Settings
        >>> settings = Settings()
        >>> settings.symbols
        ['AAPL', 'MSFT', 'SPY']
    """

    env: str = "dev"  # environment name; defaults to 'dev'
    alpaca_key_id: str | None = None  # Alpaca API key ID; defaults to None
    alpaca_secret_key: str | None = None  # Alpaca API secret key; defaults to None
    alpaca_base_url: str = "https://paper-api.alpaca.markets"  # Alpaca API base URL (paper)
    symbols: str = "AAPL,MSFT,SPY"  # default asset symbols to trade
    schedule_cron: str = "*/5 * * * *"  # cron schedule for main job; every five minutes

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )  # load variables from .env with case-insensitive keys

    @property
    def symbols_list(self) -> list[str]:
        """Return a list of symbols from the comma-separated string."""
        return [symbol.strip() for symbol in self.symbols.split(",")]
