#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import MongoClient as PyMongoClient
from pymongo.database import Collection as PyCollection
from pymongo.database import Database as PyMongoDB

from conftest import mongofullconn


def test_mongofullconn_sync():
    conn = mongofullconn(project=False)
    assert not conn.password
    assert isinstance(conn.client(), (PyMongoClient, PyMongoDB))
    db = conn.db()
    assert isinstance(db, PyMongoDB)
    assert db.name == conn.name
    col = conn.col()
    assert isinstance(col, PyCollection)
    assert col.name == conn.col_name
    if col.name in db.list_collection_names():
        col.drop()
    assert not conn.codec
    data = {db.name: col.name}
    col.insert_one(data)
    assert db.name in col.find_one(data)
    col.drop()


@pytest.mark.asyncio
async def test_mongofullconn_async():
    conn = mongofullconn()
    assert conn.password
    assert isinstance(conn.client(), (AsyncIOMotorClient, AsyncIOMotorDatabase))
    db = conn.db()
    assert isinstance(db, AsyncIOMotorDatabase)
    assert db.name == conn.name
    col = conn.col()
    assert isinstance(col, AsyncIOMotorCollection)
    assert col.name == conn.col_name
    if col.name in await db.list_collection_names():
        await col.drop()
    assert conn.codec
    data = {db.name: col.name}
    await col.insert_one(data)
    assert db.name in await col.find_one(data)
    await col.drop()
