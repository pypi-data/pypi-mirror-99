# -*- coding: utf-8 -*-

import contextvars

from bapy import ctx


def test_context():
    assert ctx.get('b') is None

    value = 1
    a = ctx('a', value, 0, int)
    assert ctx.get(a) == ctx.get('a') == value
    assert ctx.dict == {a: value}
    assert isinstance(a, contextvars.ContextVar)

    value = 2
    ctx(a, value)
    assert ctx.get(a) == ctx.get('a') == value
    assert ctx.dict == {a: value}

    assert len(ctx) == 1
    assert 'a' in ctx
    assert a in ctx
    assert 'b' not in ctx
