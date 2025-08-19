"""Simple Moving Average Crossover Strategy Engine"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

import pandas as pd


@dataclass
class Signal:
    """Trading signal with metadata"""
    symbol: str
    side: str  # 'buy' or 'sell'
    qty: float
    price_hint: float
    reason: str
    timestamp: pd.Timestamp


@dataclass
class SMAParams:
    """SMA strategy parameters"""
    fast: int = 20
    slow: int = 50
    min_volume: int = 100000


class SMAStrategy:
    """Simple Moving Average Crossover Strategy"""

    def __init__(self, params: SMAParams):
        self.params = params

    def generate_signal(
        self,
        symbol: str,
        ohlcv: pd.DataFrame,
        params: Optional[SMAParams] = None
    ) -> Optional[Signal]:
        """
        Generate trading signal based on SMA crossover

        Args:
            symbol: Stock symbol
            ohlcv: DataFrame with columns [timestamp, open, high, low, close, volume]
            params: Strategy parameters (optional, uses instance params if None)

        Returns:
            Signal object if crossover detected, None otherwise
        """
        if params is None:
            params = self.params

        if len(ohlcv) < params.slow:
            return None

        # Ensure we have required columns
        required_cols = ['timestamp', 'close', 'volume']
        if not all(col in ohlcv.columns for col in required_cols):
            return None

        # Sort by timestamp to ensure proper order
        ohlcv = ohlcv.sort_values('timestamp')

        # Calculate SMAs
        close_prices = ohlcv['close'].values
        sma_fast = pd.Series(close_prices).rolling(window=params.fast).mean()
        sma_slow = pd.Series(close_prices).rolling(window=params.slow).mean()

        # Get current and previous values for crossover detection
        if len(sma_fast) < 2 or len(sma_slow) < 2:
            return None

        current_fast = sma_fast.iloc[-1]
        current_slow = sma_slow.iloc[-1]
        prev_fast = sma_fast.iloc[-2]
        prev_slow = sma_slow.iloc[-2]

        # Check for crossover
        current_price = close_prices[-1]
        current_volume = ohlcv['volume'].iloc[-1]

        # Volume filter
        if current_volume < params.min_volume:
            return None

        # Crossover detection
        if prev_fast <= prev_slow and current_fast > current_slow:
            # Bullish crossover (fast SMA crosses above slow SMA)
            side = "buy"
            reason = f"SMA crossover: fast({params.fast})={current_fast:.2f} > slow({params.slow})={current_slow:.2f}"
        elif prev_fast >= prev_slow and current_fast < current_slow:
            # Bearish crossover (fast SMA crosses below slow SMA)
            side = "sell"
            reason = f"SMA crossover: fast({params.fast})={current_fast:.2f} < slow({params.slow})={current_slow:.2f}"
        else:
            return None

        # Simple quantity sizing: fixed dollar amount / current price
        target_notional = 1000  # $1000 per trade
        qty = int(target_notional / current_price)

        if qty <= 0:
            return None

        return Signal(
            symbol=symbol,
            side=side,
            qty=qty,
            price_hint=current_price,
            reason=reason,
            timestamp=ohlcv['timestamp'].iloc[-1]
        )


def main():
    """Test the SMA strategy with sample data"""
    import numpy as np

    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)

    # Generate sample price data with trend
    base_price = 100
    trend = np.linspace(0, 20, 100)  # Upward trend
    noise = np.random.normal(0, 2, 100)
    prices = base_price + trend + noise

    # Create sample OHLCV data
    sample_data = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': prices + np.random.uniform(0, 2, 100),
        'low': prices - np.random.uniform(0, 2, 100),
        'close': prices,
        'volume': np.random.randint(100000, 1000000, 100)
    })

    # Test strategy
    params = SMAParams(fast=10, slow=20, min_volume=50000)
    strategy = SMAStrategy(params)

    signal = strategy.generate_signal('TEST', sample_data, params)

    if signal:
        print(f"Signal generated: {signal}")
    else:
        print("No signal generated")


if __name__ == "__main__":
    main()
