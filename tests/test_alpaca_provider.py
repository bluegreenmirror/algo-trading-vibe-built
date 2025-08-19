import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from src.config import Settings
from src.data.providers import get_provider
from src.data.providers.alpaca import AlpacaDataProvider
from src.data.providers.fake_alpaca import FakeOrder
from src.data.providers.mock import MockDataProvider


class TestDataProviders(unittest.TestCase):
    def test_mock_provider_get_bars(self):
        """Test the mock data provider's get_bars method."""
        provider = MockDataProvider()
        bars = provider.get_bars("TEST", "2023-01-01", "2023-01-05")
        self.assertIsInstance(bars, pd.DataFrame)
        self.assertEqual(len(bars), 4)

    def test_mock_provider_submit_order(self):
        """Test the mock data provider's submit_order method."""
        provider = MockDataProvider()
        order = provider.submit_order("TEST", 100, "buy")
        self.assertIsInstance(order, FakeOrder)
        self.assertEqual(order.symbol, "TEST")

    def test_get_provider_returns_mock_without_keys(self):
        """Test get_provider returns MockDataProvider when keys are missing."""
        mock_settings = MagicMock(spec=Settings)
        mock_settings.alpaca_key_id = None
        mock_settings.alpaca_secret_key = None
        provider = get_provider(settings=mock_settings)
        self.assertIsInstance(provider, MockDataProvider)

    @patch("alpaca.trading.client.TradingClient")
    @patch("alpaca.data.StockHistoricalDataClient")
    def test_get_provider_returns_alpaca_with_keys(
        self, mock_data_client, mock_trading_client
    ):
        """Test get_provider returns AlpacaDataProvider when keys are present."""
        mock_settings = MagicMock(spec=Settings)
        mock_settings.alpaca_key_id = "fake_key"
        mock_settings.alpaca_secret_key = "fake_secret"
        mock_settings.alpaca_base_url = "https://paper-api.alpaca.markets"

        provider = get_provider(settings=mock_settings)
        self.assertIsInstance(provider, AlpacaDataProvider)
