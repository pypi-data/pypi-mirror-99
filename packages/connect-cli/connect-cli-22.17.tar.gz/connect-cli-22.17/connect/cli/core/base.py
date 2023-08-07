import os

import click

from connect.cli import get_version
from connect.cli.core.account.commands import grp_account
from connect.cli.core.config import pass_config
from connect.cli.core.utils import check_for_updates


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'CloudBlue Connect CLI, version {get_version()}')
    check_for_updates()
    ctx.exit()


@click.group()
@click.option(
    '--version',
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=print_version,
)
@click.option('-c', '--config-dir',
              default=os.path.join(os.path.expanduser('~'), '.ccli'),
              type=click.Path(file_okay=False),
              help='set the config directory.')
@click.option(
    '-s',
    '--silent',
    is_flag=True,
    help='Prevent the output of informational messages.',
)
@pass_config
def cli(config, config_dir, silent):
    """CloudBlue Connect Command Line Interface"""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config.load(config_dir)
    config.silent = silent


cli.add_command(grp_account)
