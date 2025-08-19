import json
import subprocess
import sys

from src.data.providers.alpaca import fetch_bars


class FakeRESTClient:
    def get_bars(self, symbols, timeframe, limit=5):
        class Bar:
            def __init__(self, i):
                self._raw = {
                    "t": f"2025-01-0{i+1}",
                    "o": 100 + i,
                    "c": 101 + i,
                    "h": 102 + i,
                    "l": 99 + i,
                    "v": 1000 + i,
                }

        return {symbol: [Bar(i) for i in range(limit)] for symbol in symbols}


def test_fetch_bars_returns_data():
    fake_client = FakeRESTClient()
    data = fetch_bars(["AAPL"], limit=3, client=fake_client)

    assert "AAPL" in data
    assert len(data["AAPL"]) == 3
    assert data["AAPL"][0].o == 100
    assert hasattr(data["AAPL"][0], "t")


def test_cli_fetch():
    # This test requires Alpaca credentials to be set in the environment
    # It will be skipped if they are not present
    import os

    if not os.environ.get("ALPACA_KEY_ID") or not os.environ.get("ALPACA_SECRET_KEY"):
        import pytest

        pytest.skip("Skipping CLI test because Alpaca credentials are not set")

    result = subprocess.run(
        [sys.executable, "-m", "src.data.providers.alpaca", "fetch", "AAPL", "--limit", "2"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert len(data) == 2
    assert "o" in data[0]
    assert "h" in data[0]
    assert "low" in data[0]
    assert "c" in data[0]
    assert "v" in data[0]
    assert "t" in data[0]
