# src/app.py
import click


@click.group()
def cli():
    """Algo Bot MVP — Sprint 1 CLI"""
    pass


@cli.command()
def hello():
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
