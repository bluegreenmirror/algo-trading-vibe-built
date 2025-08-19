from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class DataProvider(ABC):
    """Abstract base class for data providers."""

    @abstractmethod
    def get_bars(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV bars for a symbol."""
        raise NotImplementedError

    @abstractmethod
    def submit_order(self, symbol: str, notional: float, side: str) -> Any:
        """Submit a notional order."""
        raise NotImplementedError
