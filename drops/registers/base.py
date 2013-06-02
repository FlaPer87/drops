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

import logging

from oslo.config import cfg
from smartrpyc.client import pirate
from smartrpyc.server import base


OPTIONS = [
    cfg.IntOpt('worker_retries',
               default=3,
               help='Retries per worker'),
    cfg.IntOpt('worker_timeout',
               default=1000,
               help='Timeout per worker'),
]

cfg.CONF.register_opts(OPTIONS)

LOG = logging.getLogger(__name__)


class RemoteMethods(base.MethodsRegister):

    def __init__(self, conf, *args, **kwargs):
        self.conf = conf
        super(RemoteMethods, self).__init__(*args, **kwargs)

    def remote_store(self, name, method):
        raise NotImplementedError

    def remote_lookup(self, name):
        raise NotImplementedError

    def store(self, name, method):
        super(RemoteMethods, self).store(name, method)
        self.remote_store(name, method)

    def remotely(self, client, name):
        def method_proxy(request, *args, **kwargs):
            return getattr(client, name)(*args, **kwargs)
        return method_proxy

    def lookup(self, name):
        try:
            LOG.debug("Attempting to load local method: %s" % name)
            method = super(RemoteMethods, self).lookup(name)
        except KeyError:
            LOG.debug("Attempting to load remote method: %s" % name)
            remote = self.remote_lookup(name)
            client = pirate.Lazy(retries=self.conf.worker_retries,
                                 timeout=self.conf.worker_timeout,
                                 address=remote)
            method = self.remotely(client, name)
        LOG.debug("Method %s found" % method)
        return method
