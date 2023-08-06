# -*- coding: utf-8 -*-
import os
import pathlib

import pytest
import setuptools
import verboselogs
from bapy import BACKUP
from bapy import bapy
from bapy import CLI
from bapy import cmd
from bapy import find_up_default
from bapy import FindUp
from bapy import getmroattr
from bapy import Path
from bapy import PathCall
from bapy import PathSuffix
from bapy import PYTHON_VERSIONS
from bapy import ScriptInstall
from bapy import SCRIPTS
from bapy import setup as project  # setup conflicts with pytest
from bapy import slot
from bapy import TEMPLATES
from bapy import TESTS
from bapy import User
from bapy.core import __file__ as core_file
from icecream import ic

core_path = Path(core_file)
file_path = Path(__file__)
script_path = ScriptInstall.path() / bapy.path.name


def test_bapy(console_script):
    assert bapy.imported() is True
    assert bapy.file == core_path
    script_path.rm()
    script_path.write_text(console_script)
    assert cmd(f'{script_path} {TESTS}', sysexec=True).stdout[0] == core_file
    script_path.rm()
    assert bapy.init == core_path.parent / '__init__.py'
    assert bapy.path == core_path.parent
    assert bapy.prefix == f'{core_path.parent.name.upper()}_'
    assert bapy.package == f'{core_path.parent.name}.{core_path.stem}'
    assert bapy.project == core_path.parent.parent


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


def test_importlib():
    assert Path().importlib_contents is None
    assert Path().importlib_files is None
    assert Path().importlib_module is None
    assert Path().importlib_spec is None

    assert core_path.name in bapy.importlib_contents
    assert file_path.name in project.importlib_contents

    assert bapy.importlib_files == bapy.path
    assert project.importlib_files == project.path

    assert bapy.importlib_module.__name__ == bapy.package
    assert bapy.importlib_module.__package__ == bapy.path.name
    assert project.importlib_module.__name__ == project.package
    assert project.importlib_module.__package__ == project.path.name

    assert bapy.importlib_spec.origin == bapy.file.text
    assert project.importlib_spec.origin == project.file.text


def test_setuptools():
    bapy_kwargs = bapy.setuptools
    project_kwargs = project.setuptools
    name = bapy.project.name
    package = bapy.path.name
    assert bapy_kwargs == project_kwargs
    assert package in bapy_kwargs['entry_points']['console_scripts'][0]
    assert CLI in bapy_kwargs['entry_points']['console_scripts'][0]
    assert verboselogs.__name__ in bapy_kwargs['install_requires']
    assert f'{package}/{TEMPLATES}/*' in bapy_kwargs['package_data'][name]
    assert f'>={PYTHON_VERSIONS[0]}' in bapy_kwargs['python_requires']
    assert package in bapy_kwargs['packages']
    assert TESTS not in bapy_kwargs['packages']
    assert BACKUP not in bapy_kwargs['packages']
    assert f'{SCRIPTS}/{os.environ["BASHRC_FILE"]}' in bapy_kwargs['scripts']
    assert setuptools.__name__ in bapy_kwargs['setup_requires']
    assert pytest.__name__ in bapy_kwargs['tests_require']


def test_template():
    path = Path('/tmp')
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
    p.rm()


def test_project():
    p = Path(__file__)
    assert p.installed is None
    assert (ScriptInstall.path() / TESTS).installedbin
    assert (ScriptInstall.path() / TESTS).installedbin.text == TESTS
    tests_file = Path(__file__)
    p = tests_file.cd(tests_file.parent)
    assert p.initpy == FindUp(p / '__init__.py', p)

    b = p.cd(p.parent)
    assert b.initpy == find_up_default
    p.cd()
    assert not Path('/tmp').find_packages
    assert TESTS in project.packages
    assert TESTS not in project.packages_upload
    assert p.git == FindUp(b / PathSuffix.GIT.lowerdot, p)
    assert p.setuppy == FindUp(b / 'setup.py', p)
    assert project.project == b


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


def test_setup():
    assert project.imported() is True
    assert project.file == file_path
    assert project.init == file_path.parent / '__init__.py'
    assert project.path == file_path.parent
    assert project.prefix == f'{file_path.parent.name.upper()}_'
    assert project.package == f'{file_path.parent.name}.{file_path.stem}'
    assert project.project == file_path.parent.parent


# test_bapy()
# test_importlib()
# test_setuptools()
# test_setup()
