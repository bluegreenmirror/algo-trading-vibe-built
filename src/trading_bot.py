"""Main Trading Bot Orchestrator"""
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd

from src.config import Settings
from src.data.providers.alpaca import AlpacaDataProvider
from src.exec.order_router import OrderRouter
from src.risk.policy_engine import Limits, PolicyEngine
from src.strategy.rules_engine import SMAParams, SMAStrategy


class TradingBot:
    """Main trading bot that orchestrates strategy, policy, and execution"""

    def __init__(self, config: Settings):
        self.config = config
        self.setup_logging()
        self.setup_components()

    def setup_logging(self):
        """Setup structured logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_components(self):
        """Initialize all trading components"""
        # Initialize Alpaca provider
        if not self.config.alpaca_key_id or not self.config.alpaca_secret_key:
            self.logger.warning("Alpaca credentials not configured - using mock mode")
            self.alpaca_provider = None
        else:
            self.alpaca_provider = AlpacaDataProvider(
                api_key=self.config.alpaca_key_id,
                secret_key=self.config.alpaca_secret_key,
                base_url=self.config.alpaca_base_url
            )

        # Initialize strategy
        self.strategy = SMAStrategy(SMAParams(
            fast=20,  # TODO: make configurable
            slow=50,
            min_volume=100000
        ))

        # Initialize policy engine
        self.policy = PolicyEngine(Limits(
            max_position_per_symbol=10000.0,  # TODO: make configurable
            max_gross_notional=50000.0,
            daily_max_drawdown=1000.0,
            require_human_approval_over=2500.0
        ))

        # Initialize order router
        if self.alpaca_provider:
            self.router = OrderRouter(self.alpaca_provider)
        else:
            self.router = None

        # Parse symbols
        self.symbols = [s.strip() for s in self.config.symbols.split(',')]

        self.logger.info(f"Trading bot initialized with symbols: {self.symbols}")

    def fetch_market_data(self, symbol: str) -> pd.DataFrame:
        """Fetch market data for a symbol"""
        if not self.alpaca_provider:
            # Mock data for testing
            return self._generate_mock_data(symbol)

        try:
            bars = self.alpaca_provider.get_bars(symbol, limit=100)
            if bars is not None:
                self.logger.info(f"Fetched {len(bars)} bars for {symbol}")
                return bars
            else:
                self.logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()

    def _generate_mock_data(self, symbol: str) -> pd.DataFrame:
        """Generate mock OHLCV data for testing"""
        import numpy as np

        # Generate 100 days of mock data
        dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
        np.random.seed(hash(symbol) % 2**32)  # Deterministic but different per symbol

        base_price = 100 + hash(symbol) % 200  # Different base price per symbol
        trend = np.linspace(0, 20, 100)
        noise = np.random.normal(0, 2, 100)
        prices = base_price + trend + noise

        return pd.DataFrame({
            'timestamp': dates,
            'open': prices,
            'high': prices + np.random.uniform(0, 2, 100),
            'low': prices - np.random.uniform(0, 2, 100),
            'close': prices,
            'volume': np.random.randint(100000, 1000000, 100)
        })

    def run_trading_cycle(self):
        """Run one complete trading cycle"""
        self.logger.info("Starting trading cycle")

        for symbol in self.symbols:
            try:
                # Fetch market data
                ohlcv = self.fetch_market_data(symbol)
                if ohlcv.empty:
                    continue

                # Generate trading signal
                signal = self.strategy.generate_signal(symbol, ohlcv)
                if signal is None:
                    self.logger.info(f"No signal generated for {symbol}")
                    continue

                self.logger.info(f"Signal generated for {symbol}: {signal.side} {signal.qty} @ {signal.price_hint}")

                # Check policy
                decision = self.policy.check_order(signal)
                self.logger.info(f"Policy decision for {symbol}: {decision.status} - {decision.reason}")

                # Execute if policy allows
                if self.router:
                    result = self.router.execute(decision, signal)
                    self.logger.info(f"Execution result for {symbol}: {result.status}")

                    if result.status == "placed":
                        self.logger.info(f"Order placed for {symbol}: {result.order_id}")
                    elif result.status == "blocked":
                        self.logger.warning(f"Order blocked for {symbol}: {result.violations}")
                    elif result.status == "pending":
                        self.logger.info(f"Order pending approval for {symbol}: ${result.notional:.2f}")
                else:
                    self.logger.info(f"Mock mode: would execute {signal.side} {signal.qty} {symbol}")

            except Exception as e:
                self.logger.error(f"Error processing {symbol}: {e}")

        self.logger.info("Trading cycle completed")

    def run_continuous(self, interval_minutes: int = 5):
        """Run the bot continuously with specified interval"""
        self.logger.info(f"Starting continuous trading with {interval_minutes} minute intervals")

        try:
            while True:
                start_time = time.time()

                # Run trading cycle
                self.run_trading_cycle()

                # Wait for next cycle
                elapsed = time.time() - start_time
                sleep_time = max(0, (interval_minutes * 60) - elapsed)

                if sleep_time > 0:
                    self.logger.info(f"Sleeping for {sleep_time:.1f} seconds until next cycle")
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.logger.info("Trading bot stopped by user")
        except Exception as e:
            self.logger.error(f"Trading bot error: {e}")
            raise


def main():
    """Main entry point"""
    import click

    @click.group()
    def cli():
        """Algo Trading Bot MVP - Sprint 1"""
        pass

    @cli.command()
    @click.option('--interval', default=5, help='Trading interval in minutes')
    def run(interval: int):
        """Run the trading bot continuously"""
        config = Settings()
        bot = TradingBot(config)
        bot.run_continuous(interval)

    @cli.command()
    def test():
        """Run a single trading cycle for testing"""
        config = Settings()
        bot = TradingBot(config)
        bot.run_trading_cycle()

    cli()


if __name__ == "__main__":
    main()
