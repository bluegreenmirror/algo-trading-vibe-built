from src.config import Settings


def test_symbol_list_uses_class_defaults():
    settings = Settings()

    assert settings.symbol_list == ["AAPL", "MSFT", "SPY"]


def test_symbol_list_parses_comma_separated_string():
    settings = Settings(symbols="'AAPL', ' MSFT ', 'SPY'")

    assert settings.symbol_list == ["AAPL", "MSFT", "SPY"]


def test_symbol_list_filters_blank_entries_from_sequence():
    settings = Settings(symbols=[" AAPL ", " ", "MSFT"])

    assert settings.symbol_list == ["AAPL", "MSFT"]


def test_symbol_list_returns_empty_list_for_blank_string():
    settings = Settings(symbols="   ")

    assert settings.symbol_list == []
