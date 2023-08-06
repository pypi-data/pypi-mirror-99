#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from bson import InvalidDocument

from bapy import IPFull
from bapy import IPFullLoc
from bapy import MongoFullIPDoc
from conftest import mongofullconn


# noinspection DuplicatedCode
def test_mongofullipdoc_sync(ipsfull, ipfull_loc, ipfull_name, ipfull_ping, ipfull_ssh):
    mongofullconn(project=False)
    c = MongoFullIPDoc(**ipsfull.ping.kwargs)
    c.drop()
    with pytest.raises(InvalidDocument, match=rf".*cannot encode object.*"):
        c.update()
    c.drop()


# noinspection DuplicatedCode
@pytest.mark.asyncio
async def test_mongofullipdoc_async(ipsfull, ipfull_loc, ipfull_name, ipfull_ping, ipfull_ssh):
    mongofullconn()
    c = MongoFullIPDoc(**ipsfull.google.kwargs)
    await c.drop()
    doc_obj = await c.update_async()
    doc_dict = await c.update_async(instance=False)
    find_obj = await c.find_async()
    find_dict = await c.find_async(instance=False)
    assert isinstance(doc_obj, MongoFullIPDoc) and isinstance(doc_dict, dict)
    assert isinstance(doc_obj._id, IPFull) is isinstance(doc_dict['_id'], IPFull)
    assert isinstance(doc_obj.ip, IPFull) is isinstance(doc_dict['_id'], IPFull)
    assert isinstance(doc_obj.loc, IPFullLoc) is isinstance(doc_dict['loc'], IPFullLoc)
    assert isinstance(find_obj, MongoFullIPDoc) and isinstance(find_dict, dict)
    assert isinstance(find_obj._id, IPFull) is isinstance(find_dict['_id'], IPFull)
    assert isinstance(find_obj.ip, IPFull) is isinstance(find_dict['_id'], IPFull)
    assert isinstance(find_obj.loc, IPFullLoc) is isinstance(find_dict['loc'], IPFullLoc)
    assert str(doc_obj) == str(find_obj) == doc_obj.text == find_obj.text == ipsfull.google.text
    assert find_obj.loc.country_name == ipfull_loc['google'].country_name
    assert find_obj.name == ipfull_name['google']
    assert find_obj.ping == ipfull_ping['google']
    assert find_obj.ssh == ipfull_ssh['google']
    await c.drop()
