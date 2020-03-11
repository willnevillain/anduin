import click
from flask.cli import with_appcontext

from anduin.scripts.backfill import run as run_backfill
from anduin.scripts.empty import run as run_empty


@click.command()
@with_appcontext
def backfill():
    """Backfill static data"""
    run_backfill()


@click.command()
@with_appcontext
def empty():
    """Empty all DB tables, keeping schema intact"""
    run_empty()
