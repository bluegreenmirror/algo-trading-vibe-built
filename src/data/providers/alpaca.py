from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from src.config import Settings

try:  # Optional import; tests may inject a fake client
    from alpaca_trade_api.rest import REST, TimeFrame
except Exception:  # pragma: no cover
    REST = object  # type: ignore

    class TimeFrame:  # type: ignore
        Day = "1Day"


@dataclass(frozen=True)
class Bar:
    t: Any
    o: float
    h: float
    low: float  # Renamed l to low
    c: float
    v: float

    @classmethod
    def from_obj(cls, obj: Any) -> Bar:
        """Normalize API obj OR dict-like (including objects with ._raw) into a Bar dataclass."""
        # Prefer a dict source if present
        d = None
        if isinstance(obj, dict):
            d = obj
        elif hasattr(obj, "_raw") and isinstance(obj._raw, dict):
            d = obj._raw

        if d is not None:
            return cls(
                t=d.get("t") or d.get("timestamp") or d.get("time"),
                o=float(d.get("o", d.get("open", 0.0))),
                h=float(d.get("h", d.get("high", 0.0))),
                low=float(d.get("l", d.get("low", 0.0))),
                c=float(d.get("c", d.get("close", 0.0))),
                v=float(d.get("v", d.get("volume", 0.0))),
            )

        # Fallback to attribute-based objects
        return cls(
            t=getattr(obj, "t", getattr(obj, "timestamp", getattr(obj, "time", None))),
            o=float(getattr(obj, "o", getattr(obj, "open", 0.0))),
            h=float(getattr(obj, "h", getattr(obj, "high", 0.0))),
            low=float(getattr(obj, "l", getattr(obj, "low", 0.0))),
            c=float(getattr(obj, "c", getattr(obj, "close", 0.0))),
            v=float(getattr(obj, "v", getattr(obj, "volume", 0.0))),
        )


def _client(settings: Settings) -> REST:
    if not settings.alpaca_key_id or not settings.alpaca_secret_key:
        raise RuntimeError(
            "Missing Alpaca credentials (set ALPACA_KEY_ID and ALPACA_SECRET_KEY in .env)."
        )
    return REST(
        settings.alpaca_key_id,
        settings.alpaca_secret_key,
        base_url=settings.alpaca_base_url,
    )


def fetch_bars(
    symbols: Sequence[str] | str,
    limit: int = 5,
    timeframe: Any = None,
    *,
    client: REST | None = None,
    settings: Settings | None = None,
) -> dict[str, list[Bar]]:
    """
    Fetch recent bars for a list of symbols.
    Returns a dictionary of symbol -> list of `Bar` dataclasses.
    - Pass `client` to inject a fake client in tests.
    - If `settings` is None, a new Settings() will be used.
    """
    if settings is None:
        settings = Settings()

    symbol_list = Settings._normalize_symbols(symbols)

    if not symbol_list:
        raise ValueError("symbols must contain at least one entry")

    tf = timeframe or getattr(TimeFrame, "Day", "1Day")
    c = client or _client(settings)
    bars = c.get_bars(symbol_list, tf, limit=limit)
    return {symbol: [Bar.from_obj(b) for b in bar_list] for symbol, bar_list in bars.items()}


def submit_order(
    symbol: str,
    notional: float,
    side: str,
    *,
    client: REST | None = None,
    settings: Settings | None = None,
) -> Any:
    """
    Submit a notional order to Alpaca.

    - Pass `client` to inject a fake client in tests.
    - If `settings` is None, a new Settings() will be used.
    """
    if settings is None:
        settings = Settings()

    c = client or _client(settings)
    order = c.submit_order(
        symbol=symbol,
        notional=notional,
        side=side,
        type="market",
        time_in_force="day",
    )
    return order


def _serialize_bars(bars: dict[str, list[Bar]]) -> str:
    """Return a JSON string representing fetched bars."""

    payload: Any
    if len(bars) == 1:
        payload = [asdict(bar) for bar in next(iter(bars.values()))]
    else:
        payload = {symbol: [asdict(bar) for bar in bar_list] for symbol, bar_list in bars.items()}
    return json.dumps(payload, indent=2)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Interact with the Alpaca market data API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch OHLCV bars for one or more symbols.")
    fetch_parser.add_argument(
        "symbols", nargs="*", help="Symbols to fetch; defaults to settings.symbol_list if omitted."
    )
    fetch_parser.add_argument(
        "--limit", type=int, default=5, help="Number of bars to fetch per symbol."
    )

    args = parser.parse_args(list(argv) if argv is not None else None)

    settings = Settings()

    if args.command == "fetch":
        symbol_list = args.symbols or settings.symbol_list
        bars = fetch_bars(symbol_list, limit=args.limit, settings=settings)
        print(_serialize_bars(bars))
        return 0

    parser.error("Unsupported command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
