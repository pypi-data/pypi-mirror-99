#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import IPFull
from bapy import IPFullv4
from bapy import IPFullLoc


# noinspection DuplicatedCode
def test_ipfull_sync(ipfull_addr, ipfull_sync, ipfull_loc, ipfull_name, ipfull_ping, ipfull_ssh, ipsfull):
    assert isinstance(ipfull_sync[1], IPFull)
    assert isinstance(ipfull_sync[1].ip, IPFullv4)
    assert isinstance(ipfull_sync[1].loc, IPFullLoc)
    assert ipfull_sync[1].text == ipfull_addr[ipfull_sync[0]]
    assert ipfull_sync[1].loc == ipfull_loc[ipfull_sync[0]]
    assert ipfull_name[ipfull_sync[0]] in ipfull_sync[1].name
    assert ipfull_sync[1].ping is ipfull_ping[ipfull_sync[0]]
    if ipfull_sync[1].name != ipsfull.myipfull.name:
        assert ipfull_sync[1].ssh is ipfull_ssh[ipfull_sync[0]]


def test_ipfull_default(ipfull_addr, ipfull_default, ipfull_loc, ipfull_name, ipfull_ping, ipfull_ssh):
    assert isinstance(ipfull_default[1], IPFull)
    assert isinstance(ipfull_default[1].ip, IPFullv4)
    assert ipfull_default[1].text == ipfull_addr[ipfull_default[0]]
    assert ipfull_default[1].loc is None
    assert ipfull_default[1].name is None
    assert ipfull_default[1].ping is None
    assert ipfull_default[1].ssh is None


# noinspection DuplicatedCode,PyUnresolvedReferences
@pytest.mark.asyncio
async def test_ipfull_async(ipfull_addr, ipfull_async, ipfull_loc, ipfull_name, ipfull_ping, ipfull_ssh, ipsfull):
    assert isinstance(ipfull_async[1], IPFull)
    assert isinstance(ipfull_async[1].ip, IPFullv4)
    assert isinstance(ipfull_async[1].loc, IPFullLoc)
    assert ipfull_async[1].text == ipfull_addr[ipfull_async[0]]
    assert ipfull_async[1].loc == ipfull_loc[ipfull_async[0]]
    assert ipfull_name[ipfull_async[0]] in ipfull_async[1].name
    assert ipfull_async[1].ping is ipfull_ping[ipfull_async[0]]
    if ipfull_async[1].name != ipsfull.myipfull.name:
        assert ipfull_async[1].ssh is ipfull_ssh[ipfull_async[0]]


def test_ipfull_sort(ipsfull):
    assert sorted([ipsfull.localhost, ipsfull.myipfull, ipsfull.ssh, ipsfull.google, ipsfull.ping]) == \
           [ipsfull.google, ipsfull.ping, ipsfull.ssh, ipsfull.myipfull, ipsfull.localhost]
