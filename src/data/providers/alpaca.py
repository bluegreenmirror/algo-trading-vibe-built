"""Alpaca Market Data Provider"""
import os
from typing import Any, Optional

import pandas as pd
from src.data.providers.base import DataProvider


class AlpacaDataProvider(DataProvider):
    """Alpaca market data and trading provider."""

    def __init__(self, api_key: str, secret_key: str, paper: bool = True):
        from alpaca.data import StockHistoricalDataClient
        from alpaca.trading.client import TradingClient

        self.data_client = StockHistoricalDataClient(api_key, secret_key)
        self.trading_client = TradingClient(api_key, secret_key, paper=paper)
        print(f"✅ Connected to Alpaca API (Paper trading: {paper})")

    def get_bars(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV bars for a symbol."""
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame

        request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Day,
            limit=limit
        )
        bars = self.data_client.get_stock_bars(request_params)
        return bars.df

    def submit_order(self, symbol: str, notional: float, side: str) -> Any:
        """Submit a notional order."""
        from alpaca.trading.requests import MarketOrderRequest
        from alpaca.trading.enums import OrderSide, TimeInForce

        order_data = MarketOrderRequest(
            symbol=symbol,
            notional=notional,
            side=OrderSide(side.lower()),
            time_in_force=TimeInForce.DAY
        )
        return self.trading_client.submit_order(order_data=order_data)


def main():
    """CLI for testing the AlpacaDataProvider."""
    import click

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('symbol')
    @click.option('--limit', default=10, help='Number of bars to fetch')
    def fetch(symbol: str, limit: int):
        """Fetch and display OHLCV bars."""
        api_key = os.getenv('ALPACA_KEY_ID')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        if not api_key or not secret_key:
            print("❌ ALPACA_KEY_ID and ALPACA_SECRET_KEY must be set.")
            return

        provider = AlpacaDataProvider(api_key, secret_key)
        bars = provider.get_bars(symbol, limit)
        print(bars)

    @cli.command()
    @click.argument('symbol')
    @click.argument('notional', type=float)
    @click.argument('side', type=click.Choice(['buy', 'sell']))
    def trade(symbol: str, notional: float, side: str):
        """Submit a paper trade."""
        api_key = os.getenv('ALPACA_KEY_ID')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        if not api_key or not secret_key:
            print("❌ ALPACA_KEY_ID and ALPACA_SECRET_KEY must be set.")
            return

        provider = AlpacaDataProvider(api_key, secret_key)
        order = provider.submit_order(symbol, notional, side)
        print(order)

    cli()


if __name__ == "__main__":
    main()
