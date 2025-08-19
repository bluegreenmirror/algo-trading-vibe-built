"""Alpaca Market Data Provider"""
import os
from typing import List, Optional

import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.historical import StockBars
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest


class AlpacaDataProvider:
    """Alpaca market data provider for fetching OHLCV bars"""

    def __init__(self, api_key: str, secret_key: str, base_url: str):
        self.data_client = StockHistoricalDataClient(api_key, secret_key, base_url)
        self.trading_client = TradingClient(api_key, secret_key, base_url)

    def get_bars(
        self,
        symbol: str,
        timeframe: TimeFrame = TimeFrame.Day,
        limit: int = 100
    ) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV bars for a symbol

        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            timeframe: Time interval (default: daily)
            limit: Number of bars to fetch

        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        try:
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=timeframe,
                limit=limit
            )

            bars = self.data_client.get_stock_bars(request)

            if bars and len(bars.data) > 0:
                # Convert to pandas DataFrame
                df = bars.df
                if symbol in df.index.get_level_values(0):
                    symbol_data = df.loc[symbol]
                    return symbol_data.reset_index()

            return None

        except Exception as e:
            print(f"Error fetching bars for {symbol}: {e}")
            return None

    def place_market_order(
        self,
        symbol: str,
        side: OrderSide,
        qty: float
    ) -> Optional[str]:
        """
        Place a market order

        Args:
            symbol: Stock symbol
            side: Buy or sell
            qty: Quantity to trade

        Returns:
            Order ID if successful, None otherwise
        """
        try:
            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=side,
                time_in_force=TimeInForce.DAY
            )

            order = self.trading_client.submit_order(order_data)
            return order.id

        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")
            return None


def main():
    """CLI entry point for testing data fetching"""
    import click

    @click.command()
    @click.argument('symbol')
    @click.option('--limit', default=10, help='Number of bars to fetch')
    def fetch(symbol: str, limit: int):
        """Fetch OHLCV bars for a symbol"""
        api_key = os.getenv('ALPACA_KEY_ID')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        base_url = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

        if not api_key or not secret_key:
            click.echo("Error: ALPACA_KEY_ID and ALPACA_SECRET_KEY must be set")
            return

        provider = AlpacaDataProvider(api_key, secret_key, base_url)
        bars = provider.get_bars(symbol, limit=limit)

        if bars is not None:
            click.echo(f"Fetched {len(bars)} bars for {symbol}:")
            click.echo(bars.to_string(index=False))
        else:
            click.echo(f"Failed to fetch bars for {symbol}")

    fetch()


if __name__ == "__main__":
    main()
