# tests/test_smoke.py
from click.testing import CliRunner

from app import hello


def test_smoke():
    """Invoke the hello CLI command and ensure it runs successfully."""
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    assert "Algo Bot MVP is alive." in result.output
