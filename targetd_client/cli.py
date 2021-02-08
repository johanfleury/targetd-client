# Copyright (C) 2021 Johan Fleury <jfleury@arcaik.net>
#
# This file is part of targetd-client.
#
# targetd-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# targetd-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with targetd-client.  If not, see <https://www.gnu.org/licenses/>.

try:
    import click

    from humanize import naturalsize
    from tabulate import tabulate
except ImportError:
    import sys
    print("Please install targetd-client[cli] to use targetdctl")
    sys.exit(255)

from typing import List, Dict, Any

from targetd_client import TargetdClient, TargetdException


class Context(object):
    LOG_WARNING = 1
    LOG_INFO = 2
    LOG_DEBUG = 3

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        log_level: int,
        print_headers: bool,
    ):
        self.targetd = TargetdClient(url, username, password)
        self.log_level = log_level
        self.print_headers = print_headers

    def warning(self, msg: str):
        print(msg)

    def info(self, msg: str):
        if self.log_level < Context.LOG_INFO:
            return

        print(msg)

    def debug(self, msg: str):
        if self.log_level < Context.LOG_DEBUG:
            return

    def tabulate(self, data: List[Dict[str, Any]]):
        headers = "keys" if self.print_headers else []

        print(tabulate(self.humanize(data), headers=headers, tablefmt="plain"))

    def humanize(self, data: List[Dict[str, Any]]):
        for item in data.copy():
            for key, value in item.items():
                if "size" in key and isinstance(value, (int, float)):
                    item[key] = naturalsize(value, binary=True)

        return data


pass_context = click.make_pass_decorator(Context)


def main():
    try:
        cli()
    except TargetdException as e:
        print(e)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--debug", is_flag=True)
@click.option("--verbose", is_flag=True)
@click.option("--url", required=True)
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option(
    "--no-print-headers", "print_headers", is_flag=True, flag_value=False, default=True
)
@click.pass_context
def cli(
    ctx: click.core.Context,
    debug: True,
    verbose: True,
    url: str,
    username: str,
    password: str,
    print_headers: bool,
):
    log_level = Context.LOG_WARNING

    if debug:
        log_level = Context.LOG_DEBUG
    elif verbose:
        log_level = Context.LOG_INFO

    ctx.obj = Context(url, username, password, log_level, print_headers)


@cli.group()
def pool():
    pass


@pool.command("list")
@pass_context
def pool_list(ctx: Context):
    pools = ctx.targetd.pool_list()
    ctx.tabulate(pools)


@pool.command("get")
@pass_context
@click.argument("name")
def pool_get(ctx: Context, name: str):
    pools = [pool for pool in ctx.targetd.pool_list() if pool["name"] == name]

    if not pools:
        return

    ctx.tabulate(pools)


@cli.group()
def volume():
    pass


@volume.command("list")
@pass_context
@click.argument("pool")
def volume_list(ctx: Context, pool: str):
    volumes = ctx.targetd.vol_list(pool)
    ctx.tabulate(volumes)


@volume.command("create")
@pass_context
@click.argument("pool")
@click.argument("name")
@click.argument("size")
def volume_create(ctx: Context, pool: str, name: str, size: int):
    ctx.targetd.vol_create(pool, name, size)


@volume.command("destroy")
@pass_context
@click.argument("pool")
@click.argument("names", nargs=-1)
def volume_destroy(ctx: Context, pool: str, names: List[str]):
    for name in names:
        try:
            ctx.targetd.vol_destroy(pool, name)
        except TargetdException as e:
            if e.code != TargetdException.NOT_FOUND_VOLUME:
                raise

            ctx.info(f"Skipping non existing volume {name}")


@cli.group()
def export():
    pass


@export.command("list")
@pass_context
def export_list(ctx: Context):
    exports = ctx.targetd.export_list()
    ctx.tabulate(exports)


@export.command("create")
@pass_context
@click.argument("pool")
@click.argument("volume")
@click.argument("initiator_wwn")
@click.argument("lun")
def export_create(ctx: Context, pool: str, volume: str, initiator_wwn: str, lun: int):
    ctx.targetd.export_create(pool, volume, initiator_wwn, lun)


@export.command("destroy")
@pass_context
@click.argument("pool")
@click.argument("volume")
@click.argument("initiator_wwn")
def export_destroy(ctx: Context, pool: str, volume: str, initiator_wwn: str):
    ctx.targetd.export_destroy(pool, volume, initiator_wwn)
