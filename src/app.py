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
    """Fetch sample OHLCV bars from Alpaca (requires .env with API keys)."""
    try:
        from src.data.providers.alpaca import fetch_bars

        rows = fetch_bars(symbol=symbol, limit=limit)
        click.echo(f"Fetched {len(rows)} bars for {symbol}")
        for r in rows:
            click.echo(f"{r.t} o={r.o} h={r.h} l={r.l} c={r.c} v={r.v}")
    except Exception as e:
        click.echo(f"Error fetching bars: {e}", err=True)
        raise SystemExit(1) from e


if __name__ == "__main__":
    cli()
