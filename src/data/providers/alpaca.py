from __future__ import annotations

from dataclasses import dataclass
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
            l=float(getattr(obj, "l", getattr(obj, "low", 0.0))),
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
    symbols: list[str],
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

    tf = timeframe or getattr(TimeFrame, "Day", "1Day")
    c = client or _client(settings)
    bars = c.get_bars(symbols, tf, limit=limit)
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


if __name__ == "__main__":
    # Run with `python -m src.data.providers.alpaca`
    # Requires .env file with ALPACA_KEY_ID and ALPACA_SECRET_KEY
    print("Placing a $1 notional buy order for SPY...")
    order = submit_order(symbol="SPY", notional=1, side="buy")
    print("Order placed:", order)
