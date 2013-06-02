from __future__ import absolute_import

import redis
from oslo.config import cfg

from drops.common import decorators
from drops.persistence import base

CONF = cfg.CONF


class Driver(base.StoreBase):

    @decorators.lazy_property
    def _redis(self):
        pool = redis.ConnectionPool(host=CONF.host,
                                    port=CONF.port,
                                    db=CONF.db)
        return redis.Redis(connection_pool=pool)

    def _key(self, col, uuid):
        return "%s:%s" % (col, uuid)

    def get(self, col, uuid, **kwargs):
        return self._redis.hmget(self._key(col, uuid))

    def upsert(self, col, uuid, **kwargs):
        self._redis.hmset(self._key(col, uuid), kwargs)

    def delete(self, col, uuid, **kwargs):
        pass
