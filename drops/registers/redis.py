from __future__ import absolute_import

import random

import redis
from oslo.config import cfg

from drops.common import decorators
from drops.registers import base

OPTIONS = [
    cfg.IntOpt('port', default=6379,
               help='Redis Port'),
    cfg.IntOpt('db', default=0,
               help='Redis Database Index'),
    cfg.StrOpt('host', default='127.0.0.1',
               help='Redis Host'),
]

cfg.CONF.register_opts(OPTIONS)


class Redis(base.RemoteMethods):

    @decorators.lazy_property
    def _redis(self):
        pool = redis.ConnectionPool(host=self.conf.host,
                                    port=self.conf.port,
                                    db=self.conf.db)
        return redis.Redis(connection_pool=pool)

    def remote_store(self, name, method):
        self._redis.set("commands:%s:%s" % (name, self.conf.listen), self.conf.listen)

    def remote_lookup(self, name):
        keys = self._redis.keys("commands:%s:*" % name)
        return self._redis.get(random.choice(keys))
