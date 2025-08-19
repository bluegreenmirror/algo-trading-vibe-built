"""Factory for creating data providers."""

import os

from src.config import Settings

from .alpaca import AlpacaDataProvider
from .base import DataProvider
from .mock import MockDataProvider


def get_provider(settings: Settings | None = None) -> DataProvider:
    """Get the appropriate data provider based on the environment."""
    if settings is None:
        settings = Settings()

    if settings.alpaca_key_id and settings.alpaca_secret_key:
        return AlpacaDataProvider(
            api_key=settings.alpaca_key_id,
            secret_key=settings.alpaca_secret_key,
            paper=settings.alpaca_base_url.startswith("https://paper-api"),
        )
    return MockDataProvider()

