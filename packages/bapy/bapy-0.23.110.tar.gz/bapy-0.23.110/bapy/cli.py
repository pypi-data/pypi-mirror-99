# -*- coding: utf-8 -*-
"""CLI Module."""
from typer import Argument
from typer import Option

from .core import CMD_INSTALL_POST_DEFAULT
from .core import GIT_VERSIONS
from .core import GIT_VERSIONS_DELETE
from .core import Bump
from .core import Git
from .core import Line
from .core import app
from .core import bapy
from .core import ic
from .core import package
from .core import STDOUT
from .echo import green


@app.command(name='delete')
def _delete(keep: int = Argument(GIT_VERSIONS, help='Tags to keep.')):
    """Delete git tags."""
    bapy.setuptools()
    bapy.git.version_delete(keep=keep)


@app.command()
def install(post: bool = Option(CMD_INSTALL_POST_DEFAULT, help='Execute post install commands.')):
    """Install packages on site packages."""
    print(post)


@app.command()
def tests():
    print(package.file)


@app.command(name='all')
def _all(
        bump: Bump = Option(Bump.PATCH, autocompletion=Git.bump_values, case_sensitive=False,
                            help='Version part to raise.'),
        delete: bool = Option(GIT_VERSIONS_DELETE, help='Delete old git tags.'),
        message: str = Option(str, help='Commit message.'),
        stdout: bool = Option(STDOUT, help='Print progress messages.', )
):
    """Clean, build, upload to pypi/github and install it in site."""
    package.git.bump(bump=bump, delete=delete, message=message, stdout=stdout)
    bapy.git.bump(bump=bump, delete=delete, message=message, stdout=stdout)


@app.command()
def v():
    """Version."""
    green(package.version.installed)


@app.command()
def versions():
    """Versions: installed and latest."""
    installed = package.version.installed
    latest = package.version.latest
    Line.alt(repo=package.repo, version=f'{installed=}, {latest=}')
