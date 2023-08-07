#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from bson import InvalidDocument
from bson import ObjectId

from conftest import IPFullAddr
from conftest import MongoFullBaseTestDoc


# noinspection DuplicatedCode
def test_mongofulldoc_sync():
    client = MongoFullBaseTestDoc.get(ObjectId(), project=False)
    client.data = ['dump_test']
    client.drop()
    for c in [client, MongoFullBaseTestDoc.get(ObjectId(), project=False),
              MongoFullBaseTestDoc.get(ObjectId(), project=False, type_=set)]:
        if isinstance(c.data, set):
            with pytest.raises(InvalidDocument, match=rf".*set().*"):
                c.update()
        else:
            doc_obj = c.update()
            doc_dict = c.update(instance=False)
            find_obj = c.find_sync()
            find_dict = c.find_sync(instance=False)
            assert c.keys == c.asserts('keys')
            assert isinstance(doc_obj, MongoFullBaseTestDoc) and isinstance(doc_dict, dict)
            assert isinstance(doc_obj._id, ObjectId) is isinstance(doc_dict['_id'], ObjectId)
            assert isinstance(find_obj, MongoFullBaseTestDoc) and isinstance(find_dict, dict)
            assert isinstance(find_obj._id, ObjectId) is isinstance(find_dict['_id'], ObjectId)
            assert c.data == doc_obj.data == find_obj.data
            assert c.data == doc_dict['data'] == find_dict['data']
    client.drop()


# noinspection PyArgumentList,DuplicatedCode
@pytest.mark.asyncio
async def test_mongofulldoc_async():
    client = MongoFullBaseTestDoc.get(IPFullAddr().ping)
    client.data = ['dump_test_aio']
    await client.drop()
    _id = list()
    for c in [MongoFullBaseTestDoc.get(), client, MongoFullBaseTestDoc.get(IPFullAddr().myipfull, type_=set)]:
        _id.append(c._id)
        doc_obj = await c.update_async()
        doc_dict = await c.update_async(instance=False)
        find_obj = await c.find_async()
        find_dict = await c.find_async(instance=False)
        assert client.keys == c.asserts('keys')
        assert isinstance(doc_obj, MongoFullBaseTestDoc) and isinstance(doc_dict, dict)
        assert isinstance(doc_obj._id, str) is isinstance(doc_dict['_id'], str)
        assert isinstance(find_obj, MongoFullBaseTestDoc) and isinstance(find_dict, dict)
        assert isinstance(find_obj._id, str) is isinstance(find_dict['_id'], str)
        assert c.data == doc_obj.data == find_obj.data
        assert c.data == doc_dict['data'] == find_dict['data']
    await client.drop()
