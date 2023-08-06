#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import inspect
from dataclasses import dataclass
from dataclasses import field as datafield
from typing import Any
from typing import NamedTuple

import environs
import git.config
from _pytest.compat import NotSetType
from bapy import *

Named = NamedTuple('Named', a=Any)


class DictA(Base):
    _a = 'a'
    clsvar = 3
    logger = setup.log

    __ignore_attr__ = ['b', ]
    __ignore_copy__ = [collections.OrderedDict, ]

    def __init__(self):
        super(DictA, self).__init__()
        # self.env = environs.Env()
        self._b = 2
        self._d = 4

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return 'b'


class DictB(Base):
    _b = 'b'
    dict_a = DictA()
    env = environs.Env()
    path = Path()


class DictC(Base):
    _a = 'a'
    clsvar = None
    f = None
    logger = setup.log

    __ignore_attr__ = ['b', ]
    __ignore_copy__ = [collections.OrderedDict, ]

    def __init__(self):
        super(DictC, self).__init__()  # self.env = environs.Env()
        self._b = [None, None]
        self._d = {None, self.f}
        self._e = collections.OrderedDict()
        self.f = 2

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return 'b'


@dataclass
class DataA(BaseData):
    a: str = 'a'
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = environs.Env()
    integer: int = datafield(default=int(), init=False)
    logger: Log = setup.log
    path: Path = Path()


def factory():
    return [setup.log, DataA(), Path(), environs.Env()]


@dataclass
class DataB(BaseData):
    b: str = 'b'
    data_a: DataA = DataA()
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = datafield(default_factory=environs.Env)
    integer: int = datafield(default=int(), init=False)
    logger: Log = setup.log
    lst: list = datafield(default_factory=factory)
    named: Named = Named(DataA)
    named_data_a: Named = Named(DataA())
    path: Path = Path()

    def __post_init__(self, log: Log):
        super().__post_init__(log)
        self.env.read_env()


@dataclass
class DataC(BaseData):
    _cprop: str = 'cprop'
    data_b: DataB = DataB()
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = datafield(default_factory=environs.Env)
    integer: int = datafield(default=int(), init=False)
    logger: Log = setup.log
    path: Path = Path()

    __ignore_kwarg__ = ['path', ]

    def __post_init__(self, log: Log):
        super().__post_init__(log)
        self.dictionary = dict(a=dict(__a='_a', _a='__a', a='__a'))

    @property
    def cprop(self):
        return self._cprop


def test_annotation():
    obj = Obj(setup.semfull)
    assert obj.initvars == ['log']
    assert isinstance(obj.initvarsdict['log'], Log)
    assert 'log' in setup.semfull.kwargs
    assert sorted(setup.semfull.keys) == sorted(obj.attrs_cls + ['log'])
    assert 'log' not in setup.semfull.defaults()
    assert setup.semfull._initvars == obj.initvarsdict
    assert SemFull._annotation('http')[0] == setup.semfull._annotation('http')[0] == int
    assert GitHub._annotation('config')[0] == setup.github._annotation('config')[
        0] == git.config.GitConfigParser
    assert MongoFullDoc._annotation('_id')[0] == str
    assert isinstance(setup.semfull._initvars['log'], Log)


# noinspection DuplicatedCode
def test_asdict():
    assert DictA().asdict == {
        '_a': 'a', '_b': 2, '_d': 4, 'a': 'a', 'clsvar': 3,
        'logger': dict(name=setup.log.name,
                       level=setup.log.level)
    }
    assert DictB().asdict == {
        '_b': 'b',
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'clsvar': 3,
            'logger': dict(name=setup.log.name, level=setup.log.level)
        },
        'env': {},
        'path': '.'
    }

    assert DictC().asdict == {
        '_a': 'a', 'clsvar': None, 'f': 2, 'logger': dict(name=setup.log.name, level=setup.log.level),
        '_b': [None, None], '_d': {None},
        '_e': collections.OrderedDict(), 'a': 'a'
    }

    assert DataA().asdict == {
        'a': 'a',
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'clsvar': 3,
            'logger': dict(name=setup.log.name, level=setup.log.level)
        },
        'dictionary': {},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'path': '.'
    }

    assert DataB().asdict == {
        'b': 'b',
        'data_a': {
            'a': 'a',
            'dict_a': {
                '_a': 'a',
                '_b': 2,
                '_d': 4,
                'a': 'a',
                'clsvar': 3,
                'logger': dict(name=setup.log.name, level=setup.log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'logger': dict(name=setup.log.name, level=setup.log.level),
            'path': '.'
        },
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'clsvar': 3,
            'logger': dict(name=setup.log.name, level=setup.log.level)
        },
        'dictionary': {},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'lst': [dict(name=setup.log.name, level=setup.log.level),
                {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        '_b': 2,
                        '_d': 4,
                        'a': 'a',
                        'clsvar': 3,
                        'logger': dict(name=setup.log.name, level=setup.log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'logger': dict(name=setup.log.name, level=setup.log.level),
                    'path': '.'
                },
                '.',
                {}],
        'named': {},
        'named_data_a': {
            'a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    '_b': 2,
                    '_d': 4,
                    'a': 'a',
                    'clsvar': 3,
                    'logger': dict(name=setup.log.name, level=setup.log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'logger': dict(name=setup.log.name, level=setup.log.level),
                'path': '.'
            }
        },
        'path': '.'
    }

    assert DataC().asdict == {
        '_cprop': 'cprop',
        'cprop': 'cprop',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    '_b': 2,
                    '_d': 4,
                    'a': 'a',
                    'clsvar': 3,
                    'logger': dict(name=setup.log.name, level=setup.log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'logger': dict(name=setup.log.name, level=setup.log.level),
                'path': '.'
            },
            'dict_a': {
                '_a': 'a',
                '_b': 2,
                '_d': 4,
                'a': 'a',
                'clsvar': 3,
                'logger': dict(name=setup.log.name, level=setup.log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'logger': dict(name=setup.log.name, level=setup.log.level),
            'lst': [dict(name=setup.log.name, level=setup.log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            '_a': 'a',
                            '_b': 2,
                            '_d': 4,
                            'a': 'a',
                            'clsvar': 3,
                            'logger': dict(name=setup.log.name, level=setup.log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'logger': dict(name=setup.log.name, level=setup.log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        '_b': 2,
                        '_d': 4,
                        'a': 'a',
                        'clsvar': 3,
                        'logger': dict(name=setup.log.name, level=setup.log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'logger': dict(name=setup.log.name, level=setup.log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'clsvar': 3,
            'logger': dict(name=setup.log.name, level=setup.log.level)
        },
        'dictionary': {'a': {'_a': '__a', 'a': '__a'}},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'path': '.'
    }


def test_attrs():
    assert DictA().attrs == ['_a', '_b', '_d', 'a', 'clsvar', 'logger']
    assert DataC().attrs == ['_cprop', 'cprop', 'data_b', 'dict_a', 'dictionary', 'env', 'integer', 'logger', 'path']


# noinspection DuplicatedCode
def test_defaults():
    assert DictA.defaults(nested=False) == DictA().defaults(nested=False)
    assert DictA.defaults(nested=False) == {'_a': 'a', 'clsvar': 3, 'logger': setup.log}

    assert DataA.defaults() == {
        'a': 'a',
        'dict_a': {'_a': 'a', 'clsvar': 3, 'logger': dict(name=setup.log.name, level=setup.log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'path': '.'
    }

    # noinspection DuplicatedCode
    assert DataB.defaults() == {
        'b': 'b',
        'data_a': {
            'a': 'a',
            'dict_a': {
                '_a': 'a', 'clsvar': 3,
                'logger': dict(name=setup.log.name, level=setup.log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'logger': dict(name=setup.log.name, level=setup.log.level),
            'path': '.'
        },
        'dict_a': {'_a': 'a', 'clsvar': 3, 'logger': dict(name=setup.log.name, level=setup.log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'lst': [dict(name=setup.log.name, level=setup.log.level),
                {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a', 'clsvar': 3, 'logger': dict(name=setup.log.name,
                                                               level=setup.log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'logger': dict(name=setup.log.name, level=setup.log.level),
                    'path': '.'
                },
                '.',
                {}],
        'named': {},
        'named_data_a': {
            'a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    'clsvar': 3,
                    'logger': dict(name=setup.log.name, level=setup.log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'logger': dict(name=setup.log.name, level=setup.log.level),
                'path': '.'
            }
        },
        'path': '.'
    }

    assert DataC.defaults() == {
        '_cprop': 'cprop',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    'clsvar': 3,
                    'logger': dict(name=setup.log.name, level=setup.log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'logger': dict(name=setup.log.name, level=setup.log.level),
                'path': '.'
            },
            'dict_a': {
                '_a': 'a', 'clsvar': 3,
                'logger': dict(name=setup.log.name, level=setup.log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'logger': dict(name=setup.log.name, level=setup.log.level),
            'lst': [dict(name=setup.log.name, level=setup.log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            '_a': 'a',
                            'clsvar': 3,
                            'logger': dict(name=setup.log.name, level=setup.log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'logger': dict(name=setup.log.name, level=setup.log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        'clsvar': 3,
                        'logger': dict(name=setup.log.name, level=setup.log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'logger': dict(name=setup.log.name, level=setup.log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {'_a': 'a', 'clsvar': 3, 'logger': dict(name=setup.log.name, level=setup.log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'path': '.'
    }


def test_depth():
    assert Obj(DataC.defaults()['dict_a']).dict
    assert not Obj(DataC.defaults(nested=False)['dict_a']).dict
    assert isinstance(DataC.defaults(nested=False)['dict_a'], DictA)
    assert isinstance(Obj(DictB, depth=1).asdict()['dict_a'].logger, Log)
    assert isinstance(Obj(DataC(), depth=2).asdict()['data_b']['data_a'], DataA)


def test_enum():
    assert Obj(NotSetType).enumenumcls
    assert not Obj(NotSetType).enumenuminstance
    assert not Obj(NotSetType).enumcls
    assert not Obj(NotSetType).enuminstance

    assert not Obj(NotSetType.token).enumenumcls
    assert Obj(NotSetType.token).enumenuminstance
    assert not Obj(NotSetType.token).enumcls
    assert not Obj(NotSetType.token).enuminstance

    assert Obj(AttributeKind).enumenumcls
    assert not Obj(AttributeKind).enumenuminstance
    assert Obj(AttributeKind).enumcls
    assert not Obj(AttributeKind).enuminstance

    assert not Obj(AttributeKind.DATA).enumenumcls
    assert Obj(AttributeKind.DATA).enumenuminstance
    assert not Obj(AttributeKind.DATA).enumcls
    assert Obj(AttributeKind.DATA).enuminstance


def test_get():
    assert Obj(DataA).getcls == Obj(DataA()).getcls
    assert Obj(DataB()).mro == (Obj(DataB).getcls, Obj(BaseData).getcls, Obj(Base).getcls, type(object()))
    assert Obj('__s__').getmodule == inspect.getmodule('__s__')


def test_is():
    assert Obj(True).bool
    assert Obj(b'a').bytes
    assert Obj(lambda x: True).callable
    assert Obj(Obj).cls
    assert Obj(DataA).dataclass
    assert not Obj(DataA()).dataclass
    assert not Obj(DataA).dataclass_instance
    assert Obj(DataA()).dataclass_instance
    assert Obj(collections.defaultdict()).defaultdict
    assert Obj({}).dict
    assert not Obj(Named('a')).dict_instance
    assert Obj(DataA()).dict_instance
    assert not Obj(DataB).dict_instance
    assert Obj(DataB()).dict_instance
    assert Obj({}).dlst
    assert Obj(list()).dlst
    assert Obj(set()).dlst
    assert Obj(tuple()).dlst
    assert Obj('__s__').end
    assert Obj(1.1).float
    assert Obj(1).int
    assert Obj('__s__').iterable
    assert Obj(list()).lst
    assert Obj(set()).lst
    assert Obj(tuple()).lst
    assert not Obj(dict()).lst
    assert Obj(list()).mlst
    assert Obj(set()).mlst
    assert Obj(tuple()).mlst
    assert Obj(dict()).mlst
    assert not Obj(1).mlst
    assert Obj(dict()).mlst
    assert Obj(collections).module
    assert Obj(collections.UserDict({})).mutablemapping
    assert Obj(Named('a')).namedtuple
    assert Obj(collections.OrderedDict({})).ordereddict
    assert Obj(lambda x: True).routine
    assert Obj(set()).set
    assert not Obj('').set
    assert Obj('__s__').start
    assert Obj('_s__', swith='_').start
    assert Obj('__s__').str
    assert not Obj('__s__').tuple
    assert Obj(Named('a')).tuple


def test_kwargs():
    assert isinstance(DataC().kwargs['data_b'], DataB)
    assert isinstance(DataC().kwargs['env'], environs.Env)
    assert isinstance(DataC().kwargs['logger'], Log)
    assert DataC().kwargs.get('path') is None


def test_kwargs_dict():
    assert isinstance(DataC().kwargs_dict['data_b'], dict)
    assert isinstance(DataC().kwargs_dict['env'], dict)
    assert isinstance(DataC().kwargs_dict['logger'], dict)
    assert DataC().kwargs_dict.get('path') is None


def test_public():
    assert DataC().public == {
        'cprop': 'cprop',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    'a': 'a',
                    'clsvar': 3,
                    'logger': dict(name=setup.log.name, level=setup.log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'logger': dict(name=setup.log.name, level=setup.log.level),
                'path': '.'
            },
            'dict_a': {
                'a': 'a', 'clsvar': 3,
                'logger': dict(name=setup.log.name, level=setup.log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'logger': dict(name=setup.log.name, level=setup.log.level),
            'lst': [dict(name=setup.log.name, level=setup.log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            'a': 'a',
                            'clsvar': 3,
                            'logger': dict(name=setup.log.name, level=setup.log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'logger': dict(name=setup.log.name, level=setup.log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        'a': 'a',
                        'clsvar': 3,
                        'logger': dict(name=setup.log.name, level=setup.log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'logger': dict(name=setup.log.name, level=setup.log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {'a': 'a', 'clsvar': 3, 'logger': dict(name=setup.log.name, level=setup.log.level)},
        'dictionary': {'a': {'a': '__a'}},
        'env': {},
        'integer': 0,
        'logger': dict(name=setup.log.name, level=setup.log.level),
        'path': '.'
    }
