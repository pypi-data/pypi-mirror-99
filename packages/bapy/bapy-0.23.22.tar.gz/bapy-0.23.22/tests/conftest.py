#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples:
    Parametrize:
        Alt 1:  pytest_generate_tests() and addr():
                    def test_all_generate_tests(addr):
                        assert IPFull(addr).text == addr
        Alt 2:  addr() only:
                    @pytest.mark.parametrize('addr', IPFullAddr._fields, indirect=True)
                    def test_all_parametrize(addr):
                        assert IPFull(addr).text == addr
"""
import dataclasses
import inspect
# import logging
# from collections import namedtuple
# from typing import Optional
# from typing import Union
#
# import bapy
import pytest
# from bapy import IPFull
# from bapy import IPFullLoc
# from bapy import MongoFullConn
# from bapy import myipfull
# from bapy import Path
# from bapy import setup_bapy
#
#
# def pytest_generate_tests(metafunc):
#     if metafunc.function.__name__ in ['test_ipfull_sync', 'test_ipfull_async', 'test_ipfull_default'] \
#             and metafunc.module.__name__ == 'test_ipfull':
#         metafunc.parametrize(metafunc.function.__name__.removeprefix('test_'), IPFullAddr._fields, indirect=True)
#     # if 'addr' in metafunc.fixturenames:
#     #     metafunc.parametrize('addr', IPFullAddr._fields, indirect=True)
#
#
# logging.getLogger('paramiko').setLevel(logging.NOTSET)
#
# IPFullAddr = namedtuple('IPFullAddr', 'google localhost myipfull ping ssh',
#                         defaults=('8.8.8.8', '127.0.0.1', myipfull(), '24.24.23.2', '54.39.133.155'))
#
#
# @dataclasses.dataclass(eq=False)
# class MongoFullBaseTest(bapy.MongoFullBase):
#     data: Union[list, set] = None
#
#     def __post_init__(self, log: Optional[bapy.Log]):
#         super().__post_init__(log)
#
#     # noinspection PyArgumentList
#     @classmethod
#     def get(cls, _id=IPFullAddr().google, project=True, type_=list):
#         mongofullconn(project)
#         return cls(_id=_id, data=type_([mongofullconn(project).name]))
#
#     def asserts(self, key: str):
#         d = dict(keys=['_id', 'data'], data=self.data)
#         return d[key]
#
#
# @dataclasses.dataclass(eq=False)
# class MongoFullBaseTestDoc(MongoFullBaseTest, bapy.MongoFullDoc):  # Needed for mongofullconn in MongoFullBaseTest.
#
#     def __post_init__(self, log: Optional[bapy.Log]):
#         super().__post_init__(log)
#         bapy.MongoFullDoc.__post_init__(self, log)
#
#     pass
#
#
# def cd(project=True):
#     return Path().cd(setup_bapy.project) if project else Path().cd(setup_bapy.tests)
#
#
# def mongofullconn(project=True):
#     cd(project)
#     return MongoFullConn()
#
#
# # <editor-fold desc="IPFull">
# @pytest.fixture(scope='session')
# def ipfull_sync(request, ipsfull):
#     return request.param, ipsfull._asdict()[request.param]
#
#
# @pytest.fixture(scope='session')
# def ipfull_addr():
#     return IPFullAddr._field_defaults
#
#
# @pytest.fixture
# async def ipfull_async(request):
#     return request.param, IPFullAddr(*[await (IPFull(addr=addr)).post_init_aio()
#                                        for addr in IPFullAddr._field_defaults.values()])._asdict()[request.param]
#
#
# @pytest.fixture(scope='session')
# def ipfull_default(request):
#     return request.param, IPFullAddr(*[IPFull(addr=addr)
#                                        for addr in IPFullAddr._field_defaults.values()])._asdict()[request.param]
#
#
# @pytest.fixture(scope='session')
# def ipfull_loc():
#     return IPFullAddr(*[IPFullLoc(addr=addr).post_init for addr in IPFullAddr._field_defaults.values()])._asdict()
#
#
# @pytest.fixture(scope='session')
# def ipfull_name():
#     return IPFullAddr('dns.google', '1.0.0.127.in-addr.arpa', 'rima-tde', '24.24.23.2',
#                       'ns565406.ip-54-39-133.net')._asdict()
#
#
# @pytest.fixture(scope='session')
# def ipfull_ping():
#     return IPFullAddr(True, True, True, False, True)._asdict()
#
#
# @pytest.fixture(scope='session')
# def ipfull_ssh():
#     return IPFullAddr(False, False, True, False, True)._asdict()
#
#
# @pytest.fixture(scope='session')
# def ipsfull():
#     return IPFullAddr(*[IPFull(addr=addr).post_init() for addr in IPFullAddr._field_defaults.values()])
# # </editor-fold>

@pytest.fixture
def console_script():
    return f"# -*- coding: utf-8 -*-\nimport re\nimport sys\nfrom bapy import app\n\nif __name__ == '__main__':\n" \
           f"    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])\n    sys.exit(app())"
