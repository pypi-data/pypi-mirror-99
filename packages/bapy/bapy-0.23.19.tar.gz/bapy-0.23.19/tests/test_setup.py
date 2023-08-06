# -*- coding: utf-8 -*-
import inspect
import logging

from bapy import *
import bapy
import importlib
from bapy.core import __file__ as bapy_file

setup_tests = Call(filename=__file__, pypi='bapy', setup=True, test=True)


def test_setup():
    assert bootstrap in setup.fileframe.text
    assert bootstrap in setup_bapy.fileframe.text
    # noinspection PyUnresolvedReferences
    assert setup.imported is setup_bapy.imported is not setup_tests.imported
    assert setup.installed == setup_bapy.installed == setup_tests.installed == (False, None, )
    assert setup.function == setup_bapy.function != setup_tests.function
    assert setup_bapy.modname == inspect.getmodulename(bapy_file)
    assert setup.package == setup_tests.package == Path(__file__).parent.name
    assert setup_bapy.package == Path(bapy_file).parent.name
    assert setup.path == setup_tests.path == Path(__file__).parent
    assert setup_bapy.path == Path(bapy_file).parent
    assert setup.repo == setup_bapy.repo == setup_tests.repo == bapy.__name__
    assert setup.project == setup_bapy.project == setup_tests.project == Path(__file__).parent.parent


def test_env(tmp_path):
    s = Call(filename=__file__, pypi='bapy', setup=True, test=True)
    assert s.env.semfull['tests'] == SemFull.tests
    assert s.env.data['PYTHONASYNCIODEBUG'] == 0
    assert s.ic.enabled is False
    assert s.package == Path(__file__).parent.name
    assert s.env.log.log_level == log_defaults.log_level
    tmp = Path().cd(tmp_path)
    assert Path.cwd().text == tmp.text
    env = tmp / '.env'
    debug_value = 'yes'
    sem_value = 1
    debug = [f'{s.prefix}{var.upper()}={debug_value}' for var in debug_defaults._fields]
    log = [f'{s.prefix}{var.upper()}={logging.CRITICAL}' for var in log_defaults._fields]
    sem = [f'{s.prefix}{var.upper()}={sem_value}' for var in s.semfull.attrs]
    env.write_text('\n'.join(debug + log + sem))
    s = Call(filename=__file__, pypi='bapy', setup=True, test=True)
    assert s.semfull.tests[Priority.LOW]._value == sem_value
    assert s.env.data['PYTHONASYNCIODEBUG'] == 1
    assert s.ic.enabled is True
    assert s.package == Path(__file__).parent.name
    assert s.env.log.log_level == logging.CRITICAL
    tmp.cd()
