# -*- coding: utf-8 -*-
from __future__ import annotations

__all__ = (
    'IPFull',
    'IPFullLike',
    'IPFullLoc',
    'IPFullv4',
    'IPFullv6',
    'getfqdnfull',
    'ipfull_addr',
    'ipfull_loc',
    'ipfull_loc_aio',
    'myipfull',
    'pingfull',
    'pingfull_aio',
    'sort_ipfull',
    'ssh_password_full',
    'ssh_password_full_aio'
)

import asyncio
import functools
import ipaddress
import json
import shlex
import socket
import urllib.error
import urllib.request
from asyncio import as_completed
from asyncio import create_task
from asyncio import to_thread
from dataclasses import dataclass
from dataclasses import InitVar
from functools import total_ordering
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

import paramiko
from ipaddress import IPv4Address
from ipaddress import IPv6Address

from .core import *
from .libfull import *


@total_ordering
@dataclass(eq=False, repr=False)
class IPFullv4(IPv4Address):
    _ip: IPFullLike

    __ignore_attr__ = ['_ALL_ONES', 'compressed', '_constants', '_max_prefixlen', 'max_prefixlen', '_netmask_cache',
                       'packed', 'text', ]

    def __post_init__(self):
        super(IPFullv4, self).__init__(self._ip)

    @property
    def text(self) -> str:
        return self.exploded


@dataclass(eq=False, repr=False)
class IPFullv6(IPv6Address):
    _ip: IPFullLike

    __ignore_attr__ = IPFullv4.__ignore_attr__ + ['_HEXTET_COUNT', '_HEX_DIGITS', ]

    def __post_init__(self):
        super(IPFullv6, self).__init__(self._ip)

    @property
    def text(self) -> str:
        return self.exploded


IPFullLike = Union[IPFullv4, IPFullv6, IPv4Address, IPv6Address, str, bytes, int]


@dataclass
class IPFullLoc(BaseData):
    IPv4: Optional[Any] = None
    city: str = None
    country_code: str = None
    country_name: str = None
    latitude: str = None
    longitude: str = None
    postal: str = None
    state: str = None
    addr: InitVar[Any] = None

    priority: Priority = Priority.LOW

    __ignore_attr__ = ['priority', 'post_init', 'post_init_aio', ]

    def __post_init__(self, log: Log, addr: Any):
        super().__post_init__(log)
        if self.IPv4 is None and addr:
            self.IPv4 = addr
        elif self.IPv4 is None:
            self.IPv4 = myipfull()

    @property
    def ip(self) -> Optional[Any]:
        return self.IPv4

    @property
    def post_init(self) -> IPFullLoc:
        self.attrs_set(**ipfull_loc(self.IPv4))
        return self

    @property
    async def post_init_aio(self) -> IPFullLoc:
        self.attrs_set(**await ipfull_loc_aio(str(self.IPv4), priority=self.priority))
        return self

    @property
    def text(self) -> str:
        return str(self.IPv4)


@dataclass(eq=False)
class IPFull(BaseDataDescriptor):
    _id: Optional[Union[IPFull, IPFullLike]] = None
    loc: Optional[IPFullLoc] = None
    name: Optional[str] = None
    ping: Optional[bool] = None
    ssh: Optional[bool] = None
    priority: Priority = Priority.LOW

    addr: InitVar[Union[IPFullLike, IPFull]] = None

    __ignore_kwarg__ = ['priority', ]

    def __post_init__(self, log: Log, addr: Union[IPFullLike, IPFull]):
        super().__post_init__(log)
        if self._id is None and addr:
            self._id = addr
        self._id = ipfull_addr(socket.gethostbyname(str(self.ip)) if self.ip else None)

    @property
    def ip(self) -> Union[IPFullv4, IPFullv6]:
        return self._id

    def post_init(self, loc: bool = True, name: bool = True, ping_: bool = True, ssh: bool = True) -> IPFull:
        self.loc = IPFullLoc(addr=self.ip).post_init if loc else self.loc
        self.name = socket.getfqdn(self.text) if name else self.name
        self.ping = pingfull(self.ip) if ping_ else self.ping
        self.ssh = ssh_password_full(self.ip) if ssh else self.ssh
        return self

    async def post_init_aio(self, loc: bool = True, name: bool = True, ping_: bool = True, ssh: bool = True) -> IPFull:
        task = list()
        if loc:
            task.append(create_task(IPFullLoc(priority=self.priority, addr=self.ip).post_init_aio,
                                    name=f'loc-{self.text}'))
        if name:
            task.append(create_task(getfqdnfull(self.ip, priority=self.priority), name=f'name-{self.text}'))
        if ping_:
            task.append(create_task(pingfull_aio(self.ip, priority=self.priority), name=f'ping-{self.text}'))
        if ssh:
            task.append(create_task(ssh_password_full_aio(self.ip, priority=self.priority), name=f'ssh-{self.text}'))
        if task:
            for coro in as_completed([self.task(t) for t in task]):
                name, result = await coro
                setattr(self, name.split('-')[0], result)
        return self

    @staticmethod
    async def task(task: asyncio.Task) -> tuple[str, Any]:
        return task.get_name(), await task

    @property
    def text(self) -> str:
        return str(self._id)


@NapFull.OSERROR.retry_async()
async def getfqdnfull(ip: Optional[Union[IPFullLike, IPFull]], priority: Priority = Priority.LOW,
                      sem: SemFull = None) -> str:
    sem = sem if sem else setup.semfull
    return await sem.run(to_thread(socket.getfqdn, str(ip)), priority=priority, sem=Sems.SOCKET)


@functools.cache
def ipfull_addr(ip: Optional[Union[IPFullLike, IPFull]] = None) -> Union[IPFullv4, IPFullv6]:
    ip = str(ip) if ip else myipfull()
    try:
        return IPFullv4(ip)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    try:
        return IPFullv6(ip)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    raise ValueError(f'{ip} does not appear to be an IPFullv4 or IPFullv6 address')


@NapFull.HTTPJSON.retry_sync()
def ipfull_loc(ip: Optional[Union[IPFullLike, IPFull]] = None) -> dict:
    """
    IP location.

    Args:
        ip: ip.

    Returns:
        dict:
    """
    ip = str(ip) if ip else myipfull()
    with urllib.request.urlopen(f'https://geolocation-db.com/json/697de680-a737-11ea-9820-af05f4014d91/'
                                f'{ip}') as loc:
        try:
            return json.loads(loc.read().decode())
        except json.decoder.JSONDecodeError as exception:
            logger.child().warning(f'{ip}', f'{exception}')
            return dict()


async def ipfull_loc_aio(ip: Any, priority: Priority = Priority.LOW, sem: SemFull = None) -> dict:
    """
    IP location.

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        dict:
    """
    sem = sem if sem else setup.semfull
    return await sem.run(to_thread(ipfull_loc, str(ip)), priority=priority, sem=Sems.HTTP)


@NapFull.HTTPJSON.retry_sync()
def myipfull() -> str:
    return ip if (ip := urllib.request.urlopen('https://ident.me').read().decode('utf8')) else '127.0.0.1'


@NapFull.OSERROR.retry_sync()
def pingfull(ip: Any = None) -> Optional[bool]:
    """
     Pings host.

     Args:
         ip: ip.

     Returns:
         Optional[bool]:
     """
    ip = str(ip) if ip else myipfull()
    pings = 3
    cmd_out = cmd(f'sudo ping -c {pings} {shlex.quote(str(ip))}')
    if cmd_out.rc == 0:
        rv = True
    elif cmd_out.rc == 2:
        rv = False
    else:
        rv = None
    return rv


async def pingfull_aio(ip: Any = None, priority: Priority = Priority.LOW, sem: SemFull = None) -> Optional[bool]:
    """
    Pings host.

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        Optional[bool]:
    """
    sem = sem if sem else setup.semfull
    return await sem.run(to_thread(pingfull, str(ip)), priority=priority, sem=Sems.PING)


def sort_ipfull(data: Iterable[str], rv_dict: bool = False, rv_ipv4: bool = False,
                rv_base: bool = False) -> Union[list[IPv4Address], list[str], list[IPFull], dict[str, IPv4Address]]:
    """
    Sort IPs.
    Args:
        data: data.
        rv_dict: dict rv with IPv4Address.
        rv_ipv4: list rv with IPv4Address.
        rv_base: list rv with IPBase and str.

    Returns:
        Union[list[IPv4Address], list[str], dict[str, IPv4Address]]:
    """
    data = iter_split(data)
    if rv_dict or rv_ipv4 or rv_base:
        rv = sorted([ipaddress.ip_address(addr) for addr in iter_split(data)])
        if rv_dict or rv_base:
            rv = {item.exploded: item for item in rv}
            if rv_base:
                rv = [IPFull(value, key) for key, value in rv.items()]
        return rv
    return sorted(iter_split(data), key=IPv4Address)


@NapFull.OSERROR.retry_sync()
def ssh_password_full(ip: Any = None) -> Optional[bool]:
    """
    SSH password.

    Args:
        ip: ip.

    Returns:
        Optional[bool]:
    """
    ip = str(ip) if ip else myipfull()
    passwords = {str(): False, 'fake': False}
    users = dict(root=False, fake=False)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log = logger.child()
    for user in users:
        for passwd in passwords:
            while True:
                try:
                    client.connect(ip, username=user, password=passwd, look_for_keys=False, timeout=3)
                    break
                except socket.timeout:
                    # 'Unreachable'
                    users[user] = None
                    passwords[passwd] = None
                    break
                except (paramiko.ssh_exception.NoValidConnectionsError, OSError, EOFError):
                    # 'Unable to connect'
                    users[user] = None
                    passwords[passwd] = None
                    break
                except paramiko.ssh_exception.BadAuthenticationType as exception:
                    if 'publickey' in repr(exception):
                        users[user] = False
                        passwords[passwd] = False
                        break
                except paramiko.ssh_exception.AuthenticationException:
                    users[user] = True
                    passwords[passwd] = True
                    break
                except paramiko.SSHException:
                    # Quota exceeded, retrying with delay...
                    users[user] = None
                    passwords[passwd] = None
                    NapFull.OSERROR.sleep()
                    break
                except (urllib.error.URLError, OSError) as exception:
                    log.warning('Waiting for connection', f'{ip=}', f'{repr(exception)=}')
                    NapFull.OSERROR.sleep()
                    continue
                except (ConnectionResetError, paramiko.ssh_exception.SSHException, EOFError) as exception:
                    log.warning(f'Waiting for connection', f'{ip=}', f'{repr(exception)=}')
                    NapFull.OSERROR.sleep()
                    continue
                users[user] = True
                passwords[passwd] = True
                try:
                    client.exec_command('hostname;w')
                    log.critical('Connection established', f'{ip=}', f'{user=}', f'{passwd=}')
                except paramiko.ssh_exception.SSHException as exception:
                    log.error('Connection established with error ', f'{ip=}', f'{user=}', f'{passwd=}', f'{exception=}')
                break
        if users['fake'] is None and users['root'] is None:
            value = None
        elif passwords[str()] or passwords['fake'] or users['root'] or users['fake']:
            value = True
        else:
            value = False
        return value


async def ssh_password_full_aio(ip: Any = None, priority: Priority = Priority.LOW,
                                sem: SemFull = None) -> Optional[bool]:
    """
    SSH password..

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        Optional[bool]:
    """
    sem = sem if sem else setup.semfull
    return await sem.run(to_thread(ssh_password_full, str(ip)), priority=priority, sem=Sems.SSH)
