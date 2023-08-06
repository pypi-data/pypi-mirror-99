# -*- coding: utf-8 -*-
import inspect
import logging
import os
import pathlib

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
from bapy import FindUp
from bapy import getmroattr
from bapy import Git
from bapy import GIT_VERSIONS
from bapy import LogEnv
from bapy import Path
from bapy import PathCall
from bapy import PathSuffix
from bapy import Priority
from bapy import PYTHON_VERSIONS
from bapy import ScriptInstall
from bapy import SCRIPTS
from bapy import SemFull
from bapy import setup as project  # setup conflicts with pytest
from bapy import slot
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
    package = f'{name}.{modname}'
    relative = file.relative_to(top.path)
    return PathTest(file, Git.top(file), modname, name, package, path, f'{name.upper()}_', relative)


this = get_path()
core = get_path(bapy_core_file)
cli_dir = ScriptInstall.path()
cli = cli_dir / bapy.path.name


def test_bapy(console_script):
    assert bapy.imported() is True
    assert bapy.file == core.file
    cli.rm()
    cli.write_text(console_script)
    assert cmd(f'{cli} {TESTS}', sysexec=True).stdout[0] == core.file.text
    cli.rm()
    assert bapy.init == core.path / '__init__.py'
    assert bapy.path == core.path
    assert bapy.prefix == f'{core.name.upper()}_'
    assert bapy.package == core.package
    bapy.setuptools()
    assert bapy.project == core.path.parent


def test_call_rm():
    path = Path('/tmp')
    name = 'dir'
    p = path(name)
    assert p.is_dir()
    p.rm()
    assert not p.is_dir()
    name = 'file'
    p = path(name, PathCall.FILE)
    assert p.is_file()
    p.rm()
    assert not p.is_file()


def test_cd_core():
    path = Path.cwd()
    local = Path.cwd().cd('/usr/local')
    usr = local.parent
    assert usr.text == usr.str == str(usr.resolved)
    assert str(pathlib.Path.cwd()) == usr.cwd().text
    assert 'local' in local
    assert local.has('usr local')
    assert not local.has('usr root')
    assert local.cd() == path


def test_cli():
    pass


def test_env(tmp_path, pathtest):
    assert project.env.semfull['tests'] == SemFull.tests
    assert project.env.data['PYTHONASYNCIODEBUG'] == 0
    assert project.ic.enabled is False
    # noinspection PyArgumentList
    assert project.env.log.log_level == LogEnv().log_level

    tmp = Path().cd(tmp_path)
    assert Path.cwd().text == tmp.text
    env = tmp / '.env'
    debug_value = 'yes'
    sem_value = 1
    d = [f'{project.prefix}{var.upper()}={debug_value}' for var in DebugEnv._fields]
    log = [f'{project.prefix}{var.upper()}={logging.CRITICAL}' for var in LogEnv._fields]
    sem = [f'{project.prefix}{var.upper()}={sem_value}' for var in project.semfull.attrs]
    env.write_text('\n'.join(d + log + sem))
    setup = Path.setup()
    assert setup.semfull.tests[Priority.LOW]._value == sem_value
    assert setup.env.data['PYTHONASYNCIODEBUG'] == 1
    assert setup.ic.enabled is True
    assert setup.package == pathtest.package
    assert setup.env.log.log_level == logging.CRITICAL
    tmp.cd()


# noinspection PyArgumentList
def test_git(pathtest):
    project.setuptools()
    git = project.git
    assert pathtest.relative.text in git.ls
    assert f'include {pathtest.relative.text}' in (project.project / MANIFEST).read_text()
    assert git.version == VersionInfo.parse(cmd(GitCmd().tag).stdout[0].removeprefix('v'))
    delete = 1
    if len(git.versions) > GIT_VERSIONS + delete:
        total = len(git.versions)
        keep = total - delete
        version = git.version
        git.version_delete(keep=keep)
        assert len(git.versions) == keep
        assert git.version == version
    if len(git.versions) > GIT_VERSIONS + delete:
        total = len(git.versions)
        keep = total - delete
        version = git.version
        result = runner.invoke(app, [CMD_DELETE, str(delete)])
        assert result.exit_code == 0
        assert str(delete) in result.stdout
        assert len(git.versions) == keep
        assert git.version == version
    version = git.version
    git.bump(Bump.BUILD)
    previous = git.previous
    assert version == previous

    new = git.version
    git_version = cmd(GitCmd().tag).stdout[0]
    assert VersionInfo.parse(git_version.removeprefix('v')) == new
    git.delete_tag(git_version)
    assert VersionInfo.parse(cmd(GitCmd().tag).stdout[0].removeprefix('v')) == previous


def test_importlib(pathtest):
    assert Path().importlib_contents is None
    assert Path().importlib_files is None
    assert Path().importlib_module is None
    assert Path().importlib_spec is None

    assert core.file.name in bapy.importlib_contents
    assert pathtest.file.name in project.importlib_contents

    assert bapy.importlib_files == bapy.path
    assert project.importlib_files == project.path == pathtest.path

    assert bapy.importlib_module.__name__ == bapy.package
    assert bapy.importlib_module.__package__ == bapy.path.name

    assert project.importlib_module.__name__ == project.package
    assert project.importlib_module.__package__ == project.path.name

    assert bapy.importlib_spec.origin == bapy.file.text
    assert project.importlib_spec.origin == project.file.text


def test_project(pathtest):
    assert pathtest.file.installed is None
    assert (cli_dir / TESTS).installedbin
    assert (cli_dir / TESTS).installedbin.text == TESTS

    p = pathtest.file.cd(pathtest.path)
    assert p.initpy == FindUp(p / '__init__.py', p)

    b = p.cd(p.parent)
    # noinspection PyArgumentList
    assert b.initpy == FindUp()
    p.cd()

    assert not Path('/tmp').find_packages
    project.setuptools()
    assert TESTS in project.packages
    assert TESTS not in project.packages_upload
    assert p.setuppy == FindUp(b / 'setup.py', p)
    assert project.project == Git.top(b).path
    assert project.project == b


def test_setup(pathtest):
    assert project.imported() is True
    assert project.file == pathtest.file
    assert project.init == pathtest.path / '__init__.py'
    assert project.path == pathtest.path
    assert project.prefix == pathtest.prefix
    assert project.package == pathtest.package


def test_setuptools(pathtest):
    bapy.setuptools()
    project.setuptools()
    repo = bapy.repo
    package = bapy.path.name
    assert project.project == pathtest.git.path
    assert project.repo == pathtest.git.name
    assert bapy.setup_kwargs == project.setup_kwargs

    assert package in bapy.setup_kwargs['entry_points']['console_scripts'][0]
    assert CLI in bapy.setup_kwargs['entry_points']['console_scripts'][0]
    assert verboselogs.__name__ in bapy.setup_kwargs['install_requires']
    assert f'{package}/{TEMPLATES}/*' in bapy.setup_kwargs['package_data'][repo]
    assert f'>={PYTHON_VERSIONS[0]}' in bapy.setup_kwargs['python_requires']
    assert package in bapy.setup_kwargs['packages']
    assert TESTS not in bapy.setup_kwargs['packages']
    assert BACKUP not in bapy.setup_kwargs['packages']
    assert f'{SCRIPTS}/{os.environ["BASHRC_FILE"]}' in bapy.setup_kwargs['scripts']
    assert setuptools.__name__ in bapy.setup_kwargs['setup_requires']
    assert pytest.__name__ in bapy.setup_kwargs['tests_require']
    assert bapy.git.origin.text == f'{Url.lumenbiomics()}.git'


def _setuptools_initpy(r: str = None) -> str:
    r = f'REPO = "{r}"' if r else str()
    return f'import sys\n'\
           f'from bapy import setup\n' \
           f'{r}\n' \
           f'if __name__ == "__main__":\n' \
           f'    setup.setuptools()\n' \
           f'    print(getattr(setup, sys.argv[1]))\n'


def test_setuptools_installed(tmp_path, pathtest):
    tmp = Path(tmp_path)
    new_project_path = tmp(f'{TESTS}_module')
    new_project_init = new_project_path('__init__.py', PathCall.FILE)
    repo = str()
    new_project_init.write_text(_setuptools_initpy(r=repo))
    var = 'prefix'
    assert cmd(f'{new_project_init} {var}', sysexec=True).stdout[0] == f'{new_project_path.name.upper()}_'
    var = 'path'
    assert Path(cmd(f'{new_project_init} {var}', sysexec=True).stdout[0]) == new_project_path
    var = 'project'
    assert Path(cmd(f'{new_project_init} {var}', sysexec=True).stdout[0]) == User().home / new_project_path.name

    var = 'repo'
    assert cmd(f'{new_project_init} {var}', sysexec=True).stdout[0] == new_project_path.name
    new_project_init.write_text(_setuptools_initpy(r=TESTS))
    assert cmd(f'{new_project_init} {var}', sysexec=True).stdout[0] == TESTS


def test_slots():
    slots = getmroattr(Path)
    for i in Path.__slots__ + pathlib.Path.__slots__:
        assert i in slots

    with pytest.raises(TypeError):
        slot(Path, slots[0])

    with pytest.raises(AttributeError):
        slot(Path(), '_fake')
        slot(dict(), '_fake')
    assert slot(Path(), slots[0]) is not None
    assert hash(Path()) is not None
    assert slot(Path(), slots[0], getonly=False) is None
    assert slot(Path(), slots[0], getonly=False, value=2) == 2


def test_template(tmp_path):
    path = Path(tmp_path)
    p = path('templates')
    filename = 'sudoers'
    f = p(f'{filename}{PathSuffix.J2.lowerdot}', PathCall.FILE)
    name = User().name
    template = 'Defaults: {{ name }} !logfile, !syslog'
    value = f'Defaults: {name} !logfile, !syslog'
    f.write_text(template)
    assert p.j2(stream=False)[filename] == value
    p.j2(dest=p)
    assert p(filename, PathCall.FILE).read_text() == value


if ic.enabled:
    cs = f"# -*- coding: utf-8 -*-\nimport re\nimport sys\nfrom bapy import app\n\n" \
         f"if __name__ == '__main__':\n" \
         f"    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])\n" \
         f"    sys.exit(app())"

    test_bapy(cs)
    test_call_rm()
    test_cd_core()
    test_cli()
    test_env(tmppath, this)
    test_git(this)
    test_importlib(this)
    test_project(this)
    test_setup(this)
    test_setuptools(this)
    test_setuptools_installed(tmppath, this)
    test_slots()
    test_template(tmppath)
