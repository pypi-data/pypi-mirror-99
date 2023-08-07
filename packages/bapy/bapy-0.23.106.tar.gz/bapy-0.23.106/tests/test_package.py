# -*- coding: utf-8 -*-
import inspect
import logging
import os

import pytest
import setuptools
import verboselogs
from semver import VersionInfo
from typer.testing import CliRunner

from bapy import app
from bapy import BACKUP
from bapy import bapy
from bapy import CLI
from bapy import cmd
from bapy import CMD_DELETE
from bapy import DebugEnv
from bapy import FILE
from bapy import FindUp
from bapy import Git
from bapy import GIT_VERSIONS
from bapy import LogEnv
from bapy import Package
from bapy import Path
from bapy import PathSuffix
from bapy import Priority
from bapy import PYTHON_VERSIONS
from bapy import ScriptInstall
from bapy import SCRIPTS
from bapy import SemFull
from bapy import package
from bapy import TEMPLATES
from bapy import TESTS
from bapy import Url
from bapy import User
from bapy.core import __file__ as bapy_core_file
from bapy.core import Bump
from bapy.core import GitCmd
from bapy.core import MANIFEST

from conftest import PathTest
from conftest import ic
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
    p = f'{name}.{modname}'
    relative = file.relative_to(top.path)
    return PathTest(file, Git.top(file), modname, name, p, path, f'{name.upper()}_', relative)


this = get_path()
core = get_path(bapy_core_file)
cli_dir = ScriptInstall.path()
cli = cli_dir / bapy.path.name


def test_bapy(console_script):
    assert bapy.imported() is True
    assert bapy.file == core.file
    cli.rm()
    cli.write_text(console_script)
    assert core.file.text in cmd(f'{cli} {TESTS}', py=True).stdout
    cli.rm()
    assert bapy.init_py == core.path / '__init__.py'
    assert bapy.path == core.path
    assert bapy.prefix == f'{core.name.upper()}_'
    assert bapy.package == core.package
    assert bapy.project == core.path.parent


def test_cli():
    pass


def test_env(tmp_path, pathtest):
    assert package.env.semfull['tests'] == SemFull.tests
    assert package.env.data['PYTHONASYNCIODEBUG'] == 0
    assert package.ic.enabled is False
    # noinspection PyArgumentList
    assert package.env.log.log_level == LogEnv().log_level

    tmp = Path().cd(tmp_path)
    assert Path.cwd().text == tmp.text
    env = tmp / '.env'
    debug_value = 'yes'
    sem_value = 1
    d = [f'{package.prefix}{var.upper()}={debug_value}' for var in DebugEnv._fields]
    log = [f'{package.prefix}{var.upper()}={logging.CRITICAL}' for var in LogEnv._fields]
    sem = [f'{package.prefix}{var.upper()}={sem_value}' for var in package.semfull.attrs]
    env.write_text('\n'.join(d + log + sem))
    setup = Package.init()
    assert setup.semfull.tests[Priority.LOW]._value == sem_value
    assert setup.env.data['PYTHONASYNCIODEBUG'] == 1
    assert setup.ic.enabled is True
    assert setup.package == pathtest.package
    assert setup.env.log.log_level == logging.CRITICAL
    tmp.cd()


def test_importlib(pathtest):
    p = Package()

    assert p.importlib_contents is None
    assert p.importlib_files is None
    assert p.importlib_module is None
    assert p.importlib_spec is None

    assert core.file.name in bapy.importlib_contents
    assert pathtest.file.name in package.importlib_contents

    assert bapy.importlib_files == bapy.path
    assert package.importlib_files == package.path == pathtest.path

    assert bapy.importlib_module.__name__ == bapy.package
    assert bapy.importlib_module.__package__ == bapy.path.name

    assert package.importlib_module.__name__ == package.package
    assert package.importlib_module.__package__ == package.path.name

    assert bapy.importlib_spec.origin == bapy.file.text
    assert package.importlib_spec.origin == package.file.text


# noinspection PyArgumentList
def test_git(pathtest):
    git = package.git
    assert pathtest.relative.text in git.ls
    assert git.version == VersionInfo.parse(cmd(GitCmd().tag).stdout[0].removeprefix('v'))
    if tags := [f'v{version}' for version in git.versions if version.build]:
        git.delete_tag(*tags)
    delete = 1
    if len(git.versions) > GIT_VERSIONS + delete:
        total = len(git.versions)
        keep = total - delete
        version = git.version
        git.version_delete(keep=keep, stdout=False)
        assert len(git.versions) == keep
        assert git.version == version
    if len(git.versions) > GIT_VERSIONS + delete:
        total = len(git.versions)
        keep = total - delete
        version = git.version
        result = runner.invoke(app, [CMD_DELETE, str(delete)])
        assert result.exit_code == 0
        assert f'repo: {pathtest.path.parent}, deleted: {str(delete)}' in result.stderr
        assert len(git.versions) == keep
        assert git.version == version

    version = git.version
    git.bump(bump=Bump.BUILD)
    previous = git.previous
    assert version == previous

    new = git.version
    git_version = cmd(GitCmd().tag).stdout[0]
    assert VersionInfo.parse(git_version.removeprefix('v')) == new
    git.delete_tag(git_version)
    assert VersionInfo.parse(cmd(GitCmd().tag).stdout[0].removeprefix('v')) == previous


def test_package(pathtest):
    assert pathtest.file.installed is None
    assert (cli_dir / TESTS).installedbin
    assert (cli_dir / TESTS).installedbin.text == TESTS

    p = pathtest.file.cd(pathtest.path)
    p.cd(p.parent)
    p.cd()

    assert not Path('/tmp').find_packages
    assert TESTS in package.packages
    assert TESTS not in package.packages_upload

    assert package.imported() is True
    assert package.file == pathtest.file
    assert package.init_py == pathtest.path / '__init__.py'
    assert package.path == pathtest.path
    assert package.prefix == pathtest.prefix
    assert package.package == pathtest.package
    assert package.project == pathtest.git.path
    assert package.repo == pathtest.git.name
    assert bapy.git.url.text == f'{Url.lumenbiomics()}.git'


# def test_setuptools(pathtest):
#     bapy.setuptools()
#     package.setuptools()
#     repo = bapy.repo
#     name = bapy.path.name
#     assert bapy.setup_kwargs == package.setup_kwargs
#
#     assert f'include {pathtest.relative.text}' in (package.project / MANIFEST).read_text()
#
#     assert name in bapy.setup_kwargs['entry_points']['console_scripts'][0]
#     assert CLI in bapy.setup_kwargs['entry_points']['console_scripts'][0]
#     assert verboselogs.__name__ in bapy.setup_kwargs['install_requires']
#     assert f'{name}/{TEMPLATES}/*' in bapy.setup_kwargs['package_data'][repo]
#     assert f'>={PYTHON_VERSIONS[0]}' in bapy.setup_kwargs['python_requires']
#     assert name in bapy.setup_kwargs['packages']
#     assert TESTS not in bapy.setup_kwargs['packages']
#     assert BACKUP not in bapy.setup_kwargs['packages']
#     assert f'{SCRIPTS}/{os.environ["BASHRC_FILE"]}' in bapy.setup_kwargs['scripts']
#     assert setuptools.__name__ in bapy.setup_kwargs['setup_requires']
#     assert pytest.__name__ in bapy.setup_kwargs['tests_require']


def _test_installed(r: str = None) -> str:
    r = f'REPO = "{r}"' if r else str()
    return f'import sys\n'\
           f'{r}\n' \
           f'from bapy import package\n' \
           f'if __name__ == "__main__":\n' \
           f'    print(getattr(package, sys.argv[1]))\n'


def test_installed(tmp_path, pathtest):
    tmp = Path(tmp_path)
    new_project_path = tmp(f'{TESTS}_module')
    g = Path().home() / new_project_path.name
    assert Git.toppath(g)
    g.rm()
    new_project_init = new_project_path('__init__.py', FILE)
    repo = str()
    new_project_init.write_text(_test_installed(r=repo))
    var = 'prefix'
    assert f'{new_project_path.name.upper()}_' in cmd(f'{new_project_init} {var}', py=True, exc=True).stdout
    var = 'path'
    assert new_project_path.text in cmd(f'{new_project_init} {var}', py=True).stdout
    var = 'package'
    assert new_project_path.name in cmd(f'{new_project_init} {var}', py=True).stdout
    var = 'project'
    assert (User().home / new_project_path.name).text in cmd(f'{new_project_init} {var}', py=True).stdout

    var = 'repo'
    assert new_project_path.name in cmd(f'{new_project_init} {var}', py=True).stdout
    new_project_init.write_text(_test_installed(r=TESTS))
    g.rm()
    assert TESTS in cmd(f'{new_project_init} {var}', py=True).stdout


if ic.enabled:
    cs = f"# -*- coding: utf-8 -*-\nimport re\nimport sys\nfrom bapy import app\n\n" \
         f"if __name__ == '__main__':\n" \
         f"    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])\n" \
         f"    sys.exit(app())"

    test_bapy(cs)
    test_cli()
    test_env(tmppath, this)
    test_git(this)
    test_importlib(this)
    test_package(this)
    # test_setuptools(this)
    test_installed(tmppath, this)
