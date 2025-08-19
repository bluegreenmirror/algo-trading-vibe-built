import argparse
import json

from src.config import Settings
from src.data.providers.alpaca import Bar, fetch_bars


def mock_fetch_bars(symbols: list[str], limit: int, settings: Settings) -> dict[str, list[Bar]]:
    """Returns a dictionary of symbol -> list of `Bar` dataclasses with dummy data."""
    return {
        symbol: [
            Bar(t=f"2025-01-0{i+1}", o=100 + i, h=102 + i, low=99 + i, c=101 + i, v=1000 + i)
            for i in range(limit)
        ]
        for symbol in symbols
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch market data from Alpaca.")
    parser.add_argument("action", choices=["fetch"], help="Action to perform.")
    parser.add_argument("symbols", nargs="*", help="Stock symbols to fetch data for.")
    parser.add_argument("--limit", type=int, default=5, help="Number of bars to fetch.")
    args = parser.parse_args()

    if args.action == "fetch":
        settings = Settings()
        symbols_to_fetch = args.symbols or settings.symbol_list
        if settings.env == "dev":
            bars = mock_fetch_bars(symbols_to_fetch, limit=args.limit, settings=settings)
        else:
            bars = fetch_bars(symbols_to_fetch, limit=args.limit, settings=settings)
        print(
            json.dumps(
                {symbol: [b.__dict__ for b in bar_list] for symbol, bar_list in bars.items()},
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
