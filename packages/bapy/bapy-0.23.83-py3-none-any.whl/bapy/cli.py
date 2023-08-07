# -*- coding: utf-8 -*-
"""CLI Module."""
from typer import Argument
from typer import Option

from .core import CMD_INSTALL_POST_DEFAULT
from .core import GIT_VERSIONS
from .core import Bump
from .core import Git
from .core import Line
from .core import app
from .core import bapy
from .core import package
from .echo import green


@app.command()
def delete(keep: int = Argument(GIT_VERSIONS, help='Tags to keep.')):
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


@app.command()
def upload(bump: Bump = Option(Bump.PATCH, autocompletion=Git.bump_values, case_sensitive=False,
                               help='Version part to raise.')):
    """Upload to pypi/github and install it in site."""
    bapy.setuptools()
    bapy.git.bump(bump=bump)


@app.command()
def v():
    """Version."""
    green(bapy.version.installed)


@app.command()
def versions():
    """Versions: installed and latest."""
    Line.alt(repo=bapy.repo, installed=str(bapy.version.installed), latest=str(bapy.version.latest))
