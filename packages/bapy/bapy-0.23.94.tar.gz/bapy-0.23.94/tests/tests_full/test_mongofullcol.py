#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from bson import ObjectId

from bapy import *
from conftest import IPFullAddr
from conftest import MongoFullBaseTestDoc


def test_mongofullcol_sync():
    doc1 = MongoFullBaseTestDoc.get(ObjectId(), project=False)
    doc1.data = ['dump_test']
    doc1.drop()
    col = MongoFullCol(_cls=MongoFullBaseTestDoc)
    for c in [doc1, MongoFullBaseTestDoc.get(ObjectId(), project=False)]:
        c.update()
        assert col.unique_sync(instance=False) == col.unique_sync()  # _id == _id_obj
        assert col.unique_sync('data', instance=False) == col.unique_sync('data')  # data == data_obj
    col.set_sync()
    assert col.lst == col.lst_sorted
    assert col.chain == col.chain_sorted
    assert col.obj == col.obj_sorted
    for dump in col.obj:
        assert isinstance(dump, MongoFullBaseTestDoc)
    dumps = [col.lst, col.lst_sorted, col.obj, col.obj_sorted]
    assert col.chain['data'][0] == doc1.data
    assert sum(map(len, dumps)) == 2 * len(dumps)
    assert col.dct == col.dct_sorted
    assert Chain(*col.dct.values())['data'] == col.chain['data']
    doc1.drop()


# noinspection DuplicatedCode,PyArgumentList
@pytest.mark.asyncio
async def test_mongofullcol_async():
    doc1 = MongoFullBaseTestDoc.get(IPFullAddr().ping)
    doc1.data = ['dump_test_aio']
    await doc1.drop()
    col = MongoFullCol(_cls=MongoFullBaseTestDoc)
    _id = list()
    for c in [MongoFullBaseTestDoc.get(), doc1, MongoFullBaseTestDoc.get(IPFullAddr().myipfull, type_=set)]:
        _id.append(c._id)
        await c.update_async()
        assert await col.unique_async(instance=False) == await col.unique_async()  # _id == _id_obj
    sort_id = sorted(_id)
    await col.set_async()

    index = 0
    for i in col.lst:
        assert i.get('_id') == _id[index]
        index += 1

    index = 0
    for i in col.lst_sorted:
        assert i.get('_id') == sort_id[index]
        index += 1

    index = 0
    for i in col.obj:
        assert i._id == _id[index]
        index += 1

    index = 0
    for i in col.obj_sorted:
        assert i._id == sort_id[index]
        index += 1

    assert col.chain_sorted['_id'] == sort_id
    assert col.chain != col.chain_sorted
    assert col.obj != col.obj_sorted
    for dump in col.obj:
        assert isinstance(dump, MongoFullBaseTestDoc)

    dumps = [col.lst, col.lst_sorted, col.obj, col.obj_sorted]
    assert col.chain['data'][1] == doc1.data
    assert sum(map(len, dumps)) == 3 * len(dumps)
    assert col.dct == col.dct_sorted
    assert list(col.dct.keys()) == _id
    assert list(col.dct_sorted.keys()) == sort_id

    assert Chain(*col.dct.values())['data'] == col.chain['data']
    await doc1.drop()
