# File: src/data/providers/alpaca.py
"""
Alpaca Market Data Provider
Provides functions to fetch market data from Alpaca's API.
Supports dependency injection for testing with fake/mock clients.
"""

from typing import Any, Dict, List


class AlpacaMarketData:
    def __init__(self, client: Any):
        """
        Initialize with an Alpaca REST client or a fake client for tests.
        """
        self.client = client

    def fetch_bars(self, symbol: str, timeframe: str = "1Day", limit: int = 5) -> List[Dict]:
        """
        Fetch bar data for the given symbol.

        Args:
            symbol (str): Stock ticker, e.g., "AAPL".
            timeframe (str): Bar timeframe (default: "1Day").
            limit (int): Number of bars to return (default: 5).

        Returns:
            List[Dict]: List of bar data dictionaries.
        """
        bars = self.client.get_bars(symbol, timeframe, limit=limit)
        return [bar._raw for bar in bars] if bars else []
