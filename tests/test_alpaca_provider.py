import pytest
from src.data.providers.alpaca import AlpacaMarketData


class FakeRESTClient:
    def get_bars(self, symbol, timeframe, limit=5):
        class Bar:
            def __init__(self, i):
                self._raw = {"t": f"2025-01-0{i+1}", "o": 100+i, "c": 101+i}

        return [Bar(i) for i in range(limit)]


def test_fetch_bars_returns_data():
    fake_client = FakeRESTClient()
    provider = AlpacaMarketData(fake_client)
    data = provider.fetch_bars("AAPL", limit=3)

    assert len(data) == 3
    assert data[0]["o"] == 100
    assert "t" in data[0]
