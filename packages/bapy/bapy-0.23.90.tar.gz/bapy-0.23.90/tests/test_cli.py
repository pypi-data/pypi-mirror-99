# -*- coding: utf-8 -*-
import inspect
import pathlib

from typer.testing import CliRunner

from bapy import app
from bapy import bapy
from bapy import FILE
from bapy import Git
from bapy import Path
from bapy import PathSuffix
from bapy import ScriptInstall
from bapy import User
from bapy.core import __file__ as bapy_core_file
from conftest import ic
from conftest import PathTest
from conftest import tmp_path as tmppath

runner = CliRunner()


def get_path(f: str = __file__) -> PathTest:
    # Pytest first import conftest so package is tests.conftest since it is the first import to bapy
    # However, run configuration first import bapy and latter imports debug from conftest.
    file = Path(f)
    top = Git.top(file)
    modname = inspect.getmodulename(f)
    path = file.parent
    name = file.parent.name
    package = f'{name}.{modname}'
    relative = file.relative_to(top.path)
    return PathTest(file, Git.top(file), modname, name, package, path, f'{name.upper()}_', relative)


this = get_path()
core = get_path(bapy_core_file)
cli_dir = ScriptInstall.path()
cli = cli_dir / bapy.path.name


def test_all():
    result = runner.invoke(app, [CMD_DELETE, str(delete)])
    assert result.exit_code == 0
    assert f'repo: {pathtest.path.parent}, deleted: {str(delete)}' in result.stderr

