# -*- coding: utf-8 -*-
from __future__ import annotations

__all__ = (
    'DaemonFullIPCol',
    'DaemonFullIPDoc',
    'MongoFullBase',
    'MongoFullClient',
    'MongoFullCol',
    'MongoFullCollection',
    'MongoFullConn',
    'MongoFullCursor',
    'MongoFullDB',
    'MongoFullDoc',
    'MongoFullFieldValue',
    'MongoFullIPCol',
    'MongoFullIPDoc',
    'MongoFullPickledBinaryDecoder',
    'MongoFullValue',
    '_ColFull',
    '_ColFullDaemon',
    '_ColFullIP',
    '_DaemonFullDoc',
    '_DocFull',
    '_MongoFullDoc',
    '_MongoFullIPDoc',
)

import pickle
import re
from dataclasses import dataclass
from dataclasses import field as datafield
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import envtoml
import psutil
from bson import Binary
from bson import CodecOptions
from bson import ObjectId
from bson.binary import USER_DEFINED_SUBTYPE
from bson.codec_options import TypeDecoder
from bson.codec_options import TypeRegistry
from libnmap.parser import NmapParser
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorCursor
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import MongoClient as PyMongoClient
from pymongo import ReturnDocument
from pymongo.cursor import Cursor as PyMongoCursor
from pymongo.database import Collection as PyCollection
from pymongo.database import Database as PyMongoDB

from .core import *
from .ipfull import *
from .libfull import *

MongoFullClient = Union[AsyncIOMotorClient, PyMongoClient]
MongoFullCollection = Union[AsyncIOMotorCollection, PyCollection]
MongoFullDB = Union[AsyncIOMotorDatabase, PyMongoDB]
MongoFullCursor = Union[AsyncIOMotorCursor, PyMongoCursor]

MongoFullValue = Optional[Union[bool, dict, list, str]]
MongoFullFieldValue = dict[str, MongoFullValue]


class MongoFullPickledBinaryDecoder(TypeDecoder):
    bson_type = Binary

    def transform_bson(self, value):
        if value.subtype == USER_DEFINED_SUBTYPE:
            # noinspection PickleLoad
            return pickle.loads(value)
        return value


@dataclass
class MongoFullConn(BaseData):
    codec: bool = None
    connectTimeoutMS: Optional[int] = 200000
    name: str = 'test'
    host: Optional[str] = '127.0.0.1'
    maxPoolSize: Optional[int] = SemFull.mongo * 2
    password: Optional[str] = str()
    port: Optional[int] = None
    retry: bool = True
    serverSelectionTimeoutMS: Optional[int] = 300000
    srv: bool = False
    username: Optional[str] = str()
    codec_options: CodecOptions = datafield(default=None, init=False)
    file: Optional[Union[Path, str]] = datafield(default=MONGO_CONF, init=False)

    __ignore_attr__ = ['col_name', 'log', ]

    def __post_init__(self, log: Log):
        super().__post_init__(log)
        self.file = Path(self.file) if Path(self.file).is_file() else setup.home / self.file \
            if (setup.home / self.file).is_file() else None
        self.attrs_set(**envtoml.load(self.file.text) if self.file else {})
        if self.codec and self.codec_options is None:
            self.codec_options = CodecOptions(type_registry=TypeRegistry(
                [MongoFullPickledBinaryDecoder()], fallback_encoder=MongoFullConn.fallback_encoder_pickle))

    @NapFull.MONGO.retry_sync()
    def client(self, db: Optional[str] = None) -> Union[MongoFullClient, MongoFullDB]:
        if self.host == '127.0.0.1' and psutil.MACOS:
            cmd('mongossh.sh')
        func = AsyncIOMotorClient if aioloop() else PyMongoClient
        return func(f'mongodb{"+srv" if self.srv else str()}://'
                    f'{str() if (u := ":".join([self.username, self.password])) == ":" else f"{u}@"}{self.host}'
                    f'{f":{self.port}" if self.port and not self.srv else str()}/{db if db else self.name}'
                    f'{"?retryWrites=true&w=majority" if self.retry else str()}',
                    connectTimeoutMS=self.connectTimeoutMS, maxPoolSize=self.maxPoolSize,
                    serverSelectionTimeoutMS=self.serverSelectionTimeoutMS).get_database(db if db else self.name)

    @NapFull.MONGO.retry_sync()
    def db(self, name: Optional[str] = None) -> MongoFullDB:
        name = name if name else self.name
        rv = self.client(db=name)
        return rv.get_database(name=name) if isinstance(rv, (AsyncIOMotorClient, PyMongoClient)) \
            else rv.client.get_database(name=name)

    @NapFull.MONGO.retry_sync()
    def col(self, name: str = None, db: Optional[str] = None,
            codec: Optional[CodecOptions] = None) -> MongoFullCollection:
        c = dict(codec_options=codec) if codec else dict(codec_options=self.codec_options) if self.codec_options else {}
        return self.db(name=db).get_collection(**dict(name=name if name else self.col_name) | c)

    @property
    def col_name(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def fallback_encoder_pickle(value) -> Binary:
        return Binary(pickle.dumps(value), USER_DEFINED_SUBTYPE)


@dataclass(eq=False)
class MongoFullBase(BaseDataDescriptor):
    _id: Union[str, ObjectId] = None
    conn: MongoFullConn = datafield(default_factory=MongoFullConn)
    priority: Priority = Priority.LOW

    __ignore_attr__ = []
    __ignore_kwarg__ = ['conn', 'log', 'priority', ]

    def __post_init__(self, log: Log):
        super().__post_init__(log)
        self.__ignore_attr__ = Obj(self).clsinspect(AttributeKind.PROPERTY)
        self.col_name = re.sub('(Doc|Col)', '', getattr(self, '_cls', self.__class__).__name__).lower()
        self.conn = self.conn if self.conn else MongoFullConn()
        self.col: MongoFullCollection = self.conn.col(self.col_name)
        self.count_documents = self.col.count_documents
        self.delete_one = self.col.delete_one
        self.delete_many = self.col.delete_many
        self.distinct = self.col.distinct
        self.drop = self.col.drop
        self.estimated_document_count = self.col.estimated_document_count
        self.find = self.col.find
        self.find_one = self.col.find_one
        self.find_one_and_delete = self.col.find_one_and_delete
        self.find_one_and_update = self.col.find_one_and_update
        self.insert_one = self.col.insert_one
        self.insert_many = self.col.insert_many
        self.update_many = self.col.update_many

    @classmethod
    def _annotation(cls, name: str) -> Optional[tuple]:
        if field := cls._fields().get(name):
            value = eval(field.type) if isinstance(field.type, str) else field.type
            return getattr(value, '__args__', (value,))

    @property
    def text(self) -> str:
        return str(self._id)


_DocFull = TypeVar('_DocFull', bound='MongoFullDoc')


@dataclass(eq=False)
class MongoFullDoc(MongoFullBase):
    _id: Union[str, ObjectId] = None

    def __post_init__(self, log: Log):
        super(MongoFullDoc, self).__post_init__(log)

    @NapFull.MONGO.retry_sync()
    def find_sync(self, instance: bool = True) -> Union[dict, MongoFullDoc, _DocFull]:
        """
        Find one _id (doc) and returns instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(self.find_one({'_id': self._id}), instance)

    @NapFull.MONGO.retry_async()
    async def find_async(self, instance: bool = True) -> Union[dict, MongoFullDoc, _DocFull]:
        """
        Find one _id (doc) and returns instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(await self.find_one(filter={'_id': self._id}), instance)

    @classmethod
    def rv(cls, doc: dict = None, instance: bool = True) -> Union[dict, MongoFullDoc, _DocFull]:
        doc = doc if doc else dict()
        rv = doc.copy()
        return cls(**rv) if instance else rv

    @NapFull.MONGO.retry_async()
    async def update_async(self, instance: bool = True) -> Union[dict, MongoFullDoc, _DocFull]:
        """
        Find one _id (doc), updates and returns and updated instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(
            await self.find_one_and_update(filter={'_id': self._id},
                                           update={'$set': await self.find_async(instance=False) | self.kwargs},
                                           return_document=ReturnDocument.AFTER, upsert=True), instance)

    @NapFull.MONGO.retry_sync()
    def update(self, instance: bool = True) -> Union[dict, MongoFullDoc, _DocFull]:
        """
        Find one _id (doc), updates and returns and updated instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(self.find_one_and_update({'_id': self._id},
                                                {'$set': self.find_sync(instance=False) | self.kwargs},
                                                return_document=ReturnDocument.AFTER, upsert=True), instance)


_MongoFullDoc = TypeVar('_MongoFullDoc', bound=MongoFullDoc)
_ColFull = TypeVar('_ColFull', bound='MongoFullCol')


@dataclass
class MongoFullCol(MongoFullBase):
    _cls: Union[Type[MongoFullDoc], Type[_MongoFullDoc]] = MongoFullDoc
    chain: Chain[dict] = datafield(default_factory=Chain)
    chain_sorted: Chain[dict] = datafield(default_factory=Chain)
    dct: dict = datafield(default_factory=dict)
    dct_sorted: dict = datafield(default_factory=dict)
    lst: list[dict] = datafield(default_factory=list)
    lst_sorted: list[dict] = datafield(default_factory=list)
    obj: list[_MongoFullDoc] = datafield(default_factory=list)
    obj_sorted: list[_MongoFullDoc] = datafield(default_factory=list)
    unique: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_obj: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_obj_sorted: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_sorted: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_text: list[str] = datafield(default_factory=list)
    unique_text_sorted: list[str] = datafield(default_factory=list)

    __ignore_attr__ = ['_id', ]

    def __post_init__(self, log: Log):
        super().__post_init__(log)

    def map(self, data: list = None, field: str = '_id', instance: bool = True,
            sort: bool = False) -> Union[list[str], list[Any]]:
        """
        Type call based on annotations of list of values.

        Args:
            field: field.
            data: data.
            instance: Returns list of _id str or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = data if data else self.unique
        if field == '_id' and self.conn.codec:
            self.unique_obj = data
        rv = data
        if (t := self._cls()._annotation(field)) and instance and not self.conn.codec and not any(
                [len(data) == 1, isinstance(data[0], (str, int, bool, bytes)), isinstance(t[0](), SeqNoStrArgs)]):
            rv = [item if isinstance(item, (*t, ObjectId)) else t[0](item) for item in data]
            if field == '_id':
                self.unique_obj = rv
        if field != '_id':
            return sorted(rv) if sort else rv
        self.unique_obj_sorted = sorted(rv)
        self.unique_text = [item if isinstance(item, (str, int)) else str(item) for item in self.unique]
        self.unique_text_sorted = sorted(self.unique_text)
        return self.unique_sorted

    def _chain(self):
        self.chain_sorted = Chain(*self.lst_sorted)
        self.chain = Chain(*self.lst)

    def _set(self, item, sort: bool = False):
        if sort:
            self.lst_sorted.append(self._cls.rv(item, instance=False))
            self.obj_sorted.append(self._cls.rv(item))
            del self.dct_sorted[item['_id']]['_id']
        else:
            self.dct[item['_id']] = item
            self.lst.append(self._cls.rv(item, instance=False))
            self.obj.append(self._cls.rv(item))
            del self.dct[item['_id']]['_id']

    @NapFull.MONGO.retry_async()
    async def set_async(self) -> Union[_ColFull, MongoFullCol]:
        for item in await self.unique_async():
            self.dct_sorted[item] = await self.find_one({'_id': item})
            self._set(self.dct_sorted[item].copy(), sort=True)

        for item in await self.find().to_list(None):
            # for item in await self.find().to_list(None):
            self._set(item)
        self._chain()
        return self

    @NapFull.MONGO.retry_sync()
    def set_sync(self) -> Union[_ColFull, MongoFullCol]:
        for item in self.unique_sync():
            self.dct_sorted[item] = self.find_one({'_id': item})
            self._set(self.dct_sorted[item].copy(), sort=True)
        for item in self.find():
            self._set(item)
        self._chain()
        return self

    @NapFull.MONGO.retry_async()
    async def unique_async(self, field: str = '_id', instance: bool = True, sort: bool = False) -> list:
        """
        Unique _id

        Args:
            field: field.
            instance: Returns list of _id str or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = await self.distinct(field)
        # data = await self.distinct(field)
        if field == '_id':
            self.unique = data
            self.unique_sorted = sorted(data)
        return self.map(data, field, instance, sort)

    @NapFull.MONGO.retry_sync()
    def unique_sync(self, field: str = '_id', instance: bool = True, sort: bool = False) -> list:
        """
        Unique _id

        Args:
            field: field.
            instance: Returns list of _id or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = self.distinct(field)
        if field == '_id':
            self.unique = data
            self.unique_sorted = sorted(data)
        return self.map(data, field, instance, sort)


@dataclass(eq=False)
class MongoFullIPDoc(IPFull, MongoFullDoc):
    _id: Optional[IPFull] = None

    def __post_init__(self, log: Log, addr: Union[IPFullLike, IPFull]):
        super().__post_init__(log=log, addr=addr)  # Only calls first class: IPFull
        MongoFullDoc.__post_init__(self, log)


_MongoFullIPDoc = TypeVar('_MongoFullIPDoc', bound=MongoFullIPDoc)
_ColFullIP = TypeVar('_ColFullIP', bound='MongoFullIPCol')


@dataclass
class MongoFullIPCol(MongoFullCol):
    _cls: Union[Type[MongoFullIPDoc], Type[_MongoFullIPDoc]] = MongoFullIPDoc

    def __post_init__(self, log: Log):
        super().__post_init__(log)


@dataclass(eq=False)
class DaemonFullIPDoc(MongoFullIPDoc):
    scan: Union[NmapParser, dict] = None

    def __post_init__(self, log: Log, addr: Union[IPFullLike, IPFull] = None):
        super().__post_init__(log, addr)


_DaemonFullDoc = TypeVar('_DaemonFullDoc', bound=DaemonFullIPDoc)
_ColFullDaemon = TypeVar('_ColFullDaemon', bound='DaemonFullIPCol')


@dataclass
class DaemonFullIPCol(MongoFullIPCol):
    _cls: Union[Type[DaemonFullIPDoc], Type[_DaemonFullDoc]] = DaemonFullIPDoc

    def __post_init__(self, log: Log):
        super().__post_init__(log)
