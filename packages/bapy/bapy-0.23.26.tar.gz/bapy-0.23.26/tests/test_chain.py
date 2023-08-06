# coding=utf-8
from collections import namedtuple

import pytest
from bapy import Chain
from bapy import ChainRV


class Test3:
    a = 2


class Test4:
    a = 2


test1 = namedtuple('Test1', 'a b')(1, 2)
test2 = namedtuple('Test2', 'a d')(3, 5)
test3 = Test3()
test4 = Test4()


def test_chainmap():
    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2))]
    chain = Chain(*maps)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 2}]
    chain = Chain(*maps, rv=ChainRV.FIRST)
    assert chain['a'] == 1
    chain = Chain(*maps, rv=ChainRV.ALL)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 1}, {'z': 2}]

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test2]
    chain = Chain(*maps)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 2}]
    chain = Chain(*maps, rv=ChainRV.FIRST)
    assert chain['a'] == 1
    chain = Chain(*maps, rv=ChainRV.ALL)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 1}, {'z': 2}, 1, 3]

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test2]
    chain = Chain(*maps)
    del chain['a']
    assert chain == Chain({'b': 2}, {'c': 3}, {'d': 4}, test1, test2)
    assert chain['a'] == [1, 3]

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test2]
    chain = Chain(*maps)
    assert chain.delete('a') == Chain({'b': 2}, {'c': 3}, {'d': 4}, test1, test2)
    assert chain.delete('a')['a'] == [1, 3]

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test2]
    chain = Chain(*maps, rv=ChainRV.FIRST)
    del chain['a']
    with pytest.raises(KeyError, match='a'):
        del maps[0]['a']
    assert chain['a'] == 2

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test2]
    chain = Chain(*maps, rv=ChainRV.FIRST)
    new = chain.delete('a')
    with pytest.raises(KeyError, match='a'):
        del maps[0]['a']
    new.delete('a')
    with pytest.raises(KeyError, match='a'):
        del maps[1]['a']
    assert new['a'] == 3

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test3]
    chain = Chain(*maps)
    del chain['a']
    assert chain[4] == []
    assert not hasattr(test3, 'a')
    chain.set('a', 9)
    assert chain['a'] == [9, 1]

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test4]
    chain = Chain(*maps)
    chain.set('j', 9)
    assert [maps[0]['j']] == chain['j'] == [9]
    chain.set('a', 10)
    assert [maps[0]['a'], 1] == chain['a'] == [maps[7].a, 1] == [10, 1]  # 1 from namedtuple

    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2)),
            test1, test4]
    chain = Chain(*maps, rv=ChainRV.FIRST)
    chain.set('a', 9)
    assert maps[0]['a'] == chain['a'] == 9
    assert maps[1]['a'] == 2
