from __future__ import absolute_import

import random

import redis

from drops.registers import base
from drops.common import config, decorators

OPTIONS = {
    'port': (6379, 'Redis Port'),
    'db': (0, 'Redis Database Index'),
    'host': ('127.0.0.1', 'Redis Host'),
}

prj = config.project("drops").from_options()
cfg = config.namespace('registers:redis').from_options(**OPTIONS)


class Redis(base.RemoteMethods):

    @decorators.lazy_property
    def redis(self):
        pool = redis.ConnectionPool(host=cfg.host,
                                    port=cfg.port,
                                    db=cfg.db)
        return redis.Redis(connection_pool=pool)

    def remote_store(self, name, method):
        self.redis.set("commands:%s:%s" % (name, prj.listen), prj.listen)

    def remote_lookup(self, name):
        keys = self.redis.keys("commands:%s:*" % name)
        return self.redis.get(random.choice(keys))
