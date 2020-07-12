import click

from asynctornado.server import bootup

@click.command()
@click.option('--delay', '-d', type=click.INT, default=10, show_default=True)
@click.option('--port', '-p', type=click.INT, default=8000, show_default=True)
def cli_bootup(port, delay):
    bootup(port, delay)
