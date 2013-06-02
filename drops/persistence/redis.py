#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

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
