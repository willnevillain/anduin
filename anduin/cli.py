import click
from flask.cli import with_appcontext

from anduin.scripts.backfill import run


@click.command()
@with_appcontext
def backfill():
    run()
