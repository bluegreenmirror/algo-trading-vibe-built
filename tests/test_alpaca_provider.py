import json
import subprocess
import sys
from typing import Any

import pytest

from src.data.providers.alpaca import Bar, _serialize_bars, fetch_bars, main


class FakeRESTClient:
    def __init__(self) -> None:
        self.latest_request: dict[str, Any] | None = None

    def get_bars(self, symbols, timeframe, limit=5):
        self.latest_request = {"symbols": symbols, "timeframe": timeframe, "limit": limit}

        class FakeBar:
            def __init__(self, i):
                self._raw = {
                    "t": f"2025-01-0{i+1}",
                    "o": 100 + i,
                    "c": 101 + i,
                    "h": 102 + i,
                    "l": 99 + i,
                    "v": 1000 + i,
                }

        return {symbol: [FakeBar(i) for i in range(limit)] for symbol in symbols}


def test_fetch_bars_returns_data():
    fake_client = FakeRESTClient()
    data = fetch_bars(["AAPL"], limit=3, client=fake_client)

    assert "AAPL" in data
    assert len(data["AAPL"]) == 3
    assert data["AAPL"][0].o == 100
    assert hasattr(data["AAPL"][0], "t")


def test_fetch_bars_accepts_string_symbol():
    fake_client = FakeRESTClient()
    data = fetch_bars("AAPL", limit=2, client=fake_client)

    assert list(data.keys()) == ["AAPL"]
    assert len(data["AAPL"]) == 2
    assert fake_client.latest_request is not None
    assert fake_client.latest_request["symbols"] == ["AAPL"]
    assert fake_client.latest_request["limit"] == 2


def test_fetch_bars_supports_multiple_symbols():
    fake_client = FakeRESTClient()
    data = fetch_bars(["AAPL", "MSFT"], limit=1, client=fake_client)

    assert set(data.keys()) == {"AAPL", "MSFT"}
    assert all(len(bars) == 1 for bars in data.values())
    assert fake_client.latest_request is not None
    assert fake_client.latest_request["symbols"] == ["AAPL", "MSFT"]
    assert fake_client.latest_request["limit"] == 1


def test_fetch_bars_requires_non_empty_symbols():
    fake_client = FakeRESTClient()

    with pytest.raises(ValueError):
        fetch_bars([], client=fake_client)


def test_serialize_bars_single_symbol_returns_list():
    payload = {"AAPL": [Bar(t="2024-01-01", o=1, h=1, low=1, c=1, v=1)]}

    serialized = json.loads(_serialize_bars(payload))

    assert isinstance(serialized, list)
    assert serialized[0]["o"] == 1


def test_serialize_bars_multiple_symbols_returns_dict():
    payload = {
        "AAPL": [Bar(t="2024-01-01", o=1, h=1, low=1, c=1, v=1)],
        "MSFT": [Bar(t="2024-01-01", o=2, h=2, low=2, c=2, v=2)],
    }

    serialized = json.loads(_serialize_bars(payload))

    assert isinstance(serialized, dict)
    assert set(serialized.keys()) == {"AAPL", "MSFT"}


def test_cli_fetch():
    # This test requires Alpaca credentials to be set in the environment
    # It will be skipped if they are not present
    import os

    if not os.environ.get("ALPACA_KEY_ID") or not os.environ.get("ALPACA_SECRET_KEY"):
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


def test_main_fetch_with_explicit_symbols(monkeypatch, capsys):
    captured: dict[str, Any] = {}

    def fake_fetch(symbols, limit, settings):
        captured["symbols"] = symbols
        return {"AAPL": [Bar(t="2024-01-01", o=1, h=1, low=1, c=1, v=1)]}

    monkeypatch.setattr("src.data.providers.alpaca.fetch_bars", fake_fetch)
    exit_code = main(["fetch", "AAPL", "--limit", "1"])

    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert isinstance(out, list)
    assert captured["symbols"] == ["AAPL"]


def test_main_fetch_without_symbols_uses_settings(monkeypatch, capsys):
    captured: dict[str, Any] = {}

    class FakeSettings:
        def __init__(self):
            self.symbol_list = ["IBM", "ORCL"]

    def fake_fetch(symbols, limit, settings):
        captured["symbols"] = symbols
        return {
            "IBM": [Bar(t="2024-01-01", o=1, h=1, low=1, c=1, v=1)],
            "ORCL": [Bar(t="2024-01-01", o=2, h=2, low=2, c=2, v=2)],
        }

    monkeypatch.setattr("src.data.providers.alpaca.Settings", FakeSettings)
    monkeypatch.setattr("src.data.providers.alpaca.fetch_bars", fake_fetch)

    exit_code = main(["fetch", "--limit", "1"])

    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert isinstance(out, dict)
    assert captured["symbols"] == ["IBM", "ORCL"]
