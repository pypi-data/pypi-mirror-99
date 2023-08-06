# -*- coding: utf-8 -*-
import pathlib

import pytest
from bapy import getmroattr
from bapy import in_slot
from bapy import Path
from bapy import Setup
from bapy import slot


def test_slot():
    slots = getmroattr(Setup)
    for i in Setup.__slots__ + Path.__slots__ + pathlib.Path.__slots__:
        assert i in slots

    with pytest.raises(TypeError):
        slot(Path, slots[0])

    assert in_slot(Path(), '_fake') is False
    assert in_slot(dict(), '_fake') is False

    assert slot(Path(), '_accessor') is not None
    assert hash(Path()) is not None
    assert slot(Path(), '_file', 2) == 2
