from config import Settings


def test_symbols_parsed_to_list():
    settings = Settings(symbols="AAPL,MSFT, SPY")
    assert settings.symbols == ["AAPL", "MSFT", "SPY"]
