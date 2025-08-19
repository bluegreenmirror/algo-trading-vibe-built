"""Mock Data Provider for local development and testing."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

from src.data.providers.base import DataProvider
from src.data.providers.fake_alpaca import FakeAlpacaAPI


class MockDataProvider(DataProvider):
    """A mock data provider that generates fake data for testing."""

    def __init__(self):
        np.random.seed(42)  # for reproducible data
        self.trading_client = FakeAlpacaAPI()
        print("✅ Initialized MockDataProvider")

    def get_bars(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        """Generate mock OHLCV data."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=limit)
        dates = pd.date_range(end=pd.Timestamp.now(), periods=limit, freq="D")

        base_price = 150 + hash(symbol) % 50
        prices = base_price + np.random.normal(0, 1, len(dates)).cumsum()

        data = []
        for price in prices:
            open_price = price + np.random.uniform(-0.5, 0.5)
            high = max(open_price, price) + np.random.uniform(0, 0.5)
            low = min(open_price, price) - np.random.uniform(0, 0.5)
            volume = np.random.randint(100_000, 5_000_000)
            data.append(
                {
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(price, 2),
                    "volume": volume,
                }
            )

        df = pd.DataFrame(data, index=dates)
        df.index.name = "timestamp"
        return df

    def submit_order(self, symbol: str, notional: float, side: str) -> Any:
        """Submit a mock notional order."""
        print(f"📦 Submitting mock order for {notional} of {symbol}")
        return self.trading_client.submit_order(
            symbol=symbol, notional=notional, side=side
        )
