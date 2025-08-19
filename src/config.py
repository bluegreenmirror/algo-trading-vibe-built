# src/config.py
"""Application configuration models.

This module provides a small ``Settings`` class used throughout the
application.  The original project relied on the thirdâparty
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
    """Application settings.

    ``symbols`` is exposed as a list for ease of use.  When a comma separated
    string is supplied (either via environment variables or directly when
    instantiating the class) the value is split and any surrounding whitespace
    is removed.
    """

    env: str = "dev"
    alpaca_key_id: str | None = None
    alpaca_secret_key: str | None = None
    alpaca_base_url: str = "https://paper-api.alpaca.markets"
    symbols: list[str] = ["AAPL", "MSFT", "SPY"]
    schedule_cron: str = "*/5 * * * *"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    def __init__(self, **data):  # type: ignore[override]
        """Initialise settings and normalise symbol input."""

        super().__init__(**data)
        if isinstance(self.symbols, str):
            self.symbols = [s.strip() for s in self.symbols.split(",") if s.strip()]
