# src/app.py
import click


@click.group()
def cli():
    """Algo Bot MVP — Sprint 1 CLI"""
    pass


@cli.command()
def hello():
    click.echo("Algo Bot MVP is alive. (Sprint 1 skeleton)")


if __name__ == "__main__":
    cli()
