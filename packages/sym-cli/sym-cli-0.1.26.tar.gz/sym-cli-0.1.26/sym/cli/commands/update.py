import click

from sym.cli.helpers.global_options import GlobalOptions

from ..helpers.updater import SymUpdater
from .sym import sym


@sym.command(short_help="Update the Sym CLI")
@click.make_pass_decorator(GlobalOptions)
def update(options: GlobalOptions) -> None:
    SymUpdater(debug=options.debug).manual_update()
