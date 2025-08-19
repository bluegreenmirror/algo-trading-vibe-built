# src/app.py
"""Command-line interface for interacting with the Algo Bot MVP project.

This module defines the root CLI group and subcommands that allow users to
interact with the project from the terminal.  At present it exposes a simple
``hello`` command for connectivity checks.
"""

import click


@click.group()
def cli():
    """Root command group for the CLI.

    Invoked when the module is executed as a script, this function registers
    subcommands and prepares the command tree. No output is produced directly,
    but it establishes the CLI's structure for downstream commands.
    """


@cli.command()
def hello():
    """Display a basic connectivity message.

    Used as a quick sanity check, this command confirms that the CLI wiring is
    functioning.  Side effects: writes a greeting to standard output via
    :func:`click.echo`.
    """
    click.echo("Algo Bot MVP is alive. (Sprint 1 skeleton)")


@cli.command("fetch-bars")
@click.option("--symbol", default="AAPL", help="Ticker symbol")
@click.option("--limit", default=5, type=int, help="Number of bars to fetch")
def fetch_bars_cmd(symbol: str, limit: int):
    """Fetch sample OHLCV bars (uses mock data if no API keys are found)."""
    try:
        from src.data.providers import get_provider

        provider = get_provider()
        bars = provider.get_bars(symbol, limit)

        if not bars.empty:
            click.echo(f"📈 Fetched {len(bars)} bars for {symbol}:")
            click.echo("=" * 60)
            click.echo(bars.to_string())
            click.echo("=" * 60)
            click.echo(f"\n📊 Summary for {symbol}:")
            click.echo(f"   Current Close: ${bars['close'].iloc[-1]:.2f}")
            click.echo(f"   Price Range: ${bars['low'].min():.2f} - ${bars['high'].max():.2f}")
        else:
            click.echo(f"❌ No data returned for {symbol}")

    except Exception as e:
        click.echo(f"Error fetching bars: {e}", err=True)
        raise SystemExit(1) from e


@cli.command("trade")
@click.option("--symbol", default="SPY", help="Ticker symbol")
@click.option("--notional", default=1, type=float, help="Notional amount to trade")
@click.option("--side", default="buy", type=click.Choice(['buy', 'sell']), help="Side of the trade")
def trade_cmd(symbol: str, notional: float, side: str):
    """Submit a sample trade (uses mock data if no API keys are found)."""
    try:
        from src.data.providers import get_provider

        provider = get_provider()
        order = provider.submit_order(symbol, notional, side)
        click.echo("\n✅ Order submitted:")
        click.echo(order)

    except Exception as e:
        click.echo(f"Error submitting order: {e}", err=True)
        raise SystemExit(1) from e


if __name__ == "__main__":
    cli()
