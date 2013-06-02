from __future__ import absolute_import

import redis

from drops.common import decorators
from drops.persistence import base


class Driver(base.StoreBase):

    def __init__(self, conf):
        self.conf = conf

    @decorators.lazy_property
    def _redis(self):
        pool = redis.ConnectionPool(host=self.conf.host,
                                    port=self.conf.port,
                                    db=self.conf.db)
        return redis.Redis(connection_pool=pool)

    def _key(self, col, uuid):
        return "%s:%s" % (col, uuid)

    def get(self, col, uuid, **kwargs):
        return self._redis.hmget(self._key(col, uuid))

    def upsert(self, col, uuid, **kwargs):
        self._redis.hmset(self._key(col, uuid), kwargs)

    def delete(self, col, uuid, **kwargs):
        pass
