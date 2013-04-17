from __future__ import absolute_import

import redis

from drops.common import config
from drops.common import decorators
from drops.persistence import base

OPTIONS = {
    'port': (6379, 'Redis Port'),
    'db': (0, 'Redis Database Index'),
    'host': ('127.0.0.1', 'Redis Host'),
}

prj = config.project("drops").from_options()
cfg = config.namespace('redis').from_options(**OPTIONS)


class Driver(base.StoreBase):

    @decorators.lazy_property
    def redis(self):
        pool = redis.ConnectionPool(host=cfg.host,
                                    port=cfg.port,
                                    db=cfg.db)
        return redis.Redis(connection_pool=pool)

    def _key(self, col, uuid):
        return "%s:%s" % (col, uuid)

    def get(self, col, uuid, **kwargs):
        return self.redis.hmget(self._key(col, uuid))

    def upsert(self, col, uuid, **kwargs):
        self.redis.hmset(self._key(col, uuid), kwargs)

    def delete(self, col, uuid, **kwargs):
        pass
