# -*- coding: utf-8 -*-
import inspect
import pathlib

from typer.testing import CliRunner

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


def test_call_rm():
    path = Path('/tmp')
    name = 'dir'
    p = path(name)
    assert p.is_dir()
    p.rm()
    assert not p.is_dir()
    name = 'file'
    p = path(name, FILE)
    assert p.is_file()
    p.rm()
    assert not p.is_file()
    path = Path('/tmp/a/a/a/a')()
    assert path.is_dir()


def test_cd():
    path = Path.cwd()
    local = Path.cwd().cd('/usr/local')
    usr = local.parent
    assert usr.text == usr.str == str(usr.resolved)
    assert str(pathlib.Path.cwd()) == usr.cwd().text
    assert 'local' in local
    assert local.has('usr local')
    assert not local.has('usr root')
    assert local.cd() == path


def test_template(tmp_path):
    path = Path(tmp_path)
    p = path('templates')
    filename = 'sudoers'
    f = p(f'{filename}{PathSuffix.J2.lowerdot}', FILE)
    name = User().name
    template = 'Defaults: {{ name }} !logfile, !syslog'
    value = f'Defaults: {name} !logfile, !syslog'
    f.write_text(template)
    assert p.j2(stream=False)[filename] == value
    p.j2(dest=p)
    assert p(filename, FILE).read_text() == value


if ic.enabled:
    cs = f"# -*- coding: utf-8 -*-\nimport re\nimport sys\nfrom bapy import app\n\n" \
         f"if __name__ == '__main__':\n" \
         f"    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])\n" \
         f"    sys.exit(app())"

    test_call_rm()
    test_cd()
    test_template(tmppath)
