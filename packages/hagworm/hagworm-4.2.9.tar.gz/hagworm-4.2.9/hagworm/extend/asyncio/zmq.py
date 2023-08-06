# -*- coding: utf-8 -*-

import zmq

from zmq.asyncio import Context

from hagworm.extend.base import ContextManager
from hagworm.extend.asyncio.base import Utils, AsyncCirculator
from hagworm.extend.asyncio.buffer import QueueBuffer


class _SocketBase(ContextManager):

    def __init__(self, name, socket_type, address, bind_mode):

        self._name = name if name else Utils.uuid1()[:8]

        self._context = Context.instance()

        self._socket = None
        self._socket_type = socket_type

        self._address = address
        self._bind_mode = bind_mode

    def _context_initialize(self):

        self.open()

    def _context_release(self):

        self.close()

    @property
    def socket(self):

        return self._socket

    def open(self, hwm=None):

        self._socket = self._context.socket(self._socket_type)

        if self._bind_mode:
            self._socket.bind(self._address)
        else:
            self._socket.connect(self._address)

        if hwm is not None:
            self._socket.set_hwm(hwm)

    def close(self):

        if not self._socket.closed:
            self._socket.close()
            self._socket = None

    async def send(self, data, noblock=False):

        result = False

        try:

            if noblock is True:
                await self._socket.send_pyobj(data, zmq.NOBLOCK)
            else:
                await self._socket.send_pyobj(data)

        except zmq.error.Again as _:
            pass

        else:
            result = True

        return result


    async def recv(self, noblock=False):

        result = None

        try:

            if noblock is True:
                result = await self._socket.recv_pyobj(zmq.NOBLOCK)
            else:
                result = await self._socket.recv_pyobj()

        except zmq.error.Again as _:
            pass

        return result


##################################################
# 订阅模式

class Subscribe(_SocketBase):

    def __init__(self, address, bind_mode=False, *, name=None, topic=r''):

        super().__init__(name, zmq.SUB, address, bind_mode)

        self._msg_topic = topic

    def open(self, hwm=None):

        super().open(hwm)

        self._socket.setsockopt_string(zmq.SUBSCRIBE, self._msg_topic)


class Publish(_SocketBase):

    def __init__(self, address, bind_mode=False, *, name=None):

        super().__init__(name, zmq.PUB, address, bind_mode)


class PublishWithBuffer(_SocketBase, QueueBuffer):

    def __init__(self, address, bind_mode=False, *, name=None, buffer_maxsize=0xffff, buffer_timeout=1):

        _SocketBase.__init__(self, name, zmq.PUB, address, bind_mode)
        QueueBuffer.__init__(self, buffer_maxsize, buffer_timeout)

    async def _run(self, data_list):

        await self._socket.send_pyobj(data_list)

    async def safe_close(self, timeout=0):

        async for _ in AsyncCirculator(timeout):
            if len(self._data_list) == 0:
                super().close()
                break

##################################################
# 请求模式


class Request(_SocketBase):

    def __init__(self, address, *, name=None):

        super().__init__(name, zmq.REQ, address, False)


class Reply(_SocketBase):

    def __init__(self, address, *, name=None):

        super().__init__(name, zmq.REP, address, True)

##################################################
# 推拉模式


class Push(_SocketBase):

    def __init__(self, address, bind_mode=False, *, name=None):

        super().__init__(name, zmq.PUSH, address, bind_mode)


class Pull(_SocketBase):

    def __init__(self, address, bind_mode=False, *, name=None):

        super().__init__(name, zmq.PULL, address, bind_mode)
