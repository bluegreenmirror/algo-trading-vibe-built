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


if __name__ == "__main__":
    cli()
