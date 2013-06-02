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
