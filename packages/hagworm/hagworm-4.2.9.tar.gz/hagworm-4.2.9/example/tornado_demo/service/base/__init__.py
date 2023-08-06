# -*- coding: utf-8 -*-

from hagworm.extend.base import Ignore, catch_error
from hagworm.extend.metaclass import Singleton
from hagworm.extend.asyncio.base import Utils, FuncCache, ShareFuture, MultiTasks
from hagworm.extend.asyncio.cache import RedisDelegate
from hagworm.extend.asyncio.database import MongoDelegate, MySQLDelegate
from hagworm.extend.process import HeartbeatChecker

from setting import ConfigStatic, ConfigDynamic


class DataSource(Singleton, RedisDelegate, MongoDelegate, MySQLDelegate):

    def __init__(self):

        RedisDelegate.__init__(self)

        MongoDelegate.__init__(
            self,
            ConfigStatic.MongoHost, ConfigStatic.MongoUser, ConfigStatic.MongoPasswd,
            min_pool_size=ConfigStatic.MongoMinConn, max_pool_size=ConfigStatic.MongoMaxConn,
            max_idle_time=3600
        )

        MySQLDelegate.__init__(self)

        self._health_checker = None

    @classmethod
    async def initialize(cls):

        inst = cls()

        inst._health_checker = HeartbeatChecker(ConfigDynamic.ServerName)

        await inst.async_init_redis(
            ConfigStatic.RedisHost, ConfigStatic.RedisPasswd,
            minsize=ConfigStatic.RedisMinConn, maxsize=ConfigStatic.RedisMaxConn,
            db=ConfigStatic.RedisBase, expire=ConfigStatic.RedisExpire,
            key_prefix=ConfigStatic.RedisKeyPrefix
        )

        if ConfigStatic.MySqlMasterServer:

            await inst.async_init_mysql_rw(
                ConfigStatic.MySqlMasterServer[0], ConfigStatic.MySqlMasterServer[1], ConfigStatic.MySqlName,
                ConfigStatic.MySqlUser, ConfigStatic.MySqlPasswd,
                minsize=ConfigStatic.MySqlMasterMinConn, maxsize=ConfigStatic.MySqlMasterMaxConn,
                echo=ConfigDynamic.Debug, pool_recycle=21600, conn_life=43200
            )

        if ConfigStatic.MySqlSlaveServer:

            await inst.async_init_mysql_ro(
                ConfigStatic.MySqlSlaveServer[0], ConfigStatic.MySqlSlaveServer[1], ConfigStatic.MySqlName,
                ConfigStatic.MySqlUser, ConfigStatic.MySqlPasswd,
                minsize=ConfigStatic.MySqlSlaveMinConn, maxsize=ConfigStatic.MySqlSlaveMaxConn,
                echo=ConfigDynamic.Debug, pool_recycle=21600, readonly=True, conn_life=43200
            )

    @classmethod
    async def release(cls):

        inst = cls()

        inst._health_checker.release()

        inst.close_mongo_pool()

        await inst.async_close_redis()
        await inst.async_close_mysql()

    @property
    def online(self):

        return self._health_checker.check()

    @ShareFuture()
    @FuncCache(ttl=30)
    async def health(self):

        result = False

        with catch_error():

            tasks = MultiTasks()

            tasks.append(self.cache_health())
            tasks.append(self.mysql_health())
            tasks.append(self.mongo_health())

            await tasks

            result = all(tasks)

            if result is True:
                self._health_checker.refresh()

        return result


class ServiceBase(Singleton, Utils):

    def __init__(self):

        self._data_source = DataSource()

    def Break(self, data=None, layers=1):

        raise Ignore(data, layers)
