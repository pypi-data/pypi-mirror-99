#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import Chain
from bapy import MongoFullIPCol
from bapy import MongoFullIPDoc
from conftest import mongofullconn


@pytest.mark.asyncio
async def test_mongofullipcol_async(ipsfull, tmpdir):
    mongofullconn()
    client = MongoFullIPDoc(**ipsfull.google.kwargs)
    await client.drop()
    col = MongoFullIPCol()
    ip = list()
    text = list()
    for c in [MongoFullIPDoc(**v.kwargs) for v in ipsfull._asdict().values()]:
        ip.append(c.ip)
        text.append(c.text)
        await c.update_async()
        assert await col.unique_async(instance=False) == await col.unique_async()  # _id == _id_obj
    sort_ip = sorted(ip)
    sort_text = sorted(text)
    await col.set_async()

    index = 0
    for i in col.lst:
        assert i.get('_id') == ip[index]
        index += 1

    index = 0
    for i in col.lst_sorted:
        assert i.get('_id') == sort_ip[index]
        index += 1

    index = 0
    for i in col.obj:
        assert i._id == ip[index]
        assert i.text == text[index]
        index += 1

    index = 0
    for i in col.obj_sorted:
        assert i._id == sort_ip[index]
        if i.text == ipsfull.google.text:
            assert i.text != sort_text[index]
        index += 1

    assert col.chain_sorted['_id'] == sort_ip
    assert col.chain != col.chain_sorted
    assert col.obj != col.obj_sorted
    for dump in col.obj:
        assert isinstance(dump, MongoFullIPDoc)

    dumps = [col.lst, col.lst_sorted, col.obj, col.obj_sorted]
    assert col.chain['loc'][0] == client.loc
    assert sum(map(len, dumps)) == 5 * len(dumps)
    assert col.dct == col.dct_sorted
    assert list(col.dct.keys()) == ip
    assert list(col.dct_sorted.keys()) == sort_ip
    assert Chain(*col.dct.values())['loc'] == col.chain['loc']
    await client.drop()
