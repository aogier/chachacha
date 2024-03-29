"""
Created on 25 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

import typing
from dataclasses import asdict

import click
import semver
from click.core import Context

from chachacha import __version__, drivers
from chachacha.drivers.kac import ChangelogFormat


class CCCGroup(click.Group):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super().__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super().get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = (
            command
            for command in super().list_commands(ctx)
            if command not in ("init", "release", "config", "version")
        )

        return ["init", "config", "release"] + sorted(commands) + ["version"]


@click.group(cls=CCCGroup)
@click.option("--filename", default="CHANGELOG.md", help="changelog filename")
@click.option("--driver", default="kac", help="changelog format driver")
@click.pass_context
def main(ctx: Context, filename: str, driver: str) -> None:

    driver = drivers.kac.ChangelogFormat(filename)

    ctx.obj = driver


@main.command(help="initialize a new file")
@click.option("--overwrite", default=False, help="overwrite", is_flag=True)
@click.pass_obj
def init(driver: ChangelogFormat, overwrite: bool) -> None:

    driver.init(overwrite)


@main.command(help='add an "added" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def added(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("added", changes)


@main.command(help='add a "changed" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def changed(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("changed", changes)


@main.command(help='add a "deprecated" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def deprecated(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("deprecated", changes)


@main.command(help='add a "removed" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def removed(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("removed", changes)


@main.command(help='add a "fixed" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def fixed(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("fixed", changes)


@main.command(help='add a "security" entry')
@click.pass_obj
@click.argument("changes", nargs=-1)
def security(driver: ChangelogFormat, changes: typing.Union[str, tuple]) -> None:

    driver.add_entry("security", changes)


def _validate_version_spec(ctx, param, value):
    if value in ["major", "minor", "patch"] or semver.VersionInfo.isvalid(value):
        return value
    else:
        raise click.BadParameter("Invalid version specification")


@main.command(short_help="release a version")
@click.argument("spec", default="patch", callback=_validate_version_spec)
@click.pass_obj
def release(driver: ChangelogFormat, spec: str) -> None:
    """
    Update the changelog to release version SPEC.

    SPEC should either be the version number to release
    or the strings "major", "minor" or "patch".
    """
    driver.release(spec)


@main.command(help="configure changelog options")
@click.option("--global", "_global", help="act globally", is_flag=True)
@click.option("--show", help="show config", is_flag=True)
@click.argument("key", default="")
@click.argument("value", default="")
@click.pass_obj
def config(
    driver: ChangelogFormat, _global: bool, show: bool, key: str, value: str
) -> None:

    config = driver.get_config(init=True)

    if not key:
        for k, v in asdict(config).items():
            print(f"{k}={v}")

    if value:
        setattr(config, key, value)
        driver.write(config=config)


@main.command(help="show version and exit")
def version():  # pragma: no cover
    print(f"v{__version__}")


if __name__ == "__main__":  # pragma: no cover
    main()  # pylint: disable=no-value-for-parameter
