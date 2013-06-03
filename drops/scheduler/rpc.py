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

import inspect

from oslo.config import cfg
from smartrpyc import server
from stevedore import driver

from drops import registers


OPTIONS = [
    cfg.ListOpt('scheduler_middleware',
                default=['persistence'],
                help='Default Middlewares'),
]

cfg.CONF.register_opts(OPTIONS)


class Commander(server.Server):

    def __init__(self, conf, *args, **kwargs):
        self.conf = conf
        self._workers = []
        self._register = registers.get_register()
        kwargs.setdefault("methods", self._register)
        super(Commander, self).__init__(*args, **kwargs)

        self._load_middleware()

    def add_worker(self, worker):
        """
        Exports methods through the RPC Api.

        :params worker: Resource's instance to register.
        """

        funcs = filter(lambda x: not x.startswith("_"), dir(worker))

        for name in funcs:
            meth = getattr(worker, name)

            if not inspect.ismethod(meth):
                continue

            self._register.register(meth)

        self._workers.append(worker)

    def bind(self):
        super(Commander, self).bind(self.conf.listen)

    def _load_middleware(self):
        for mid in self.conf.scheduler_middleware:
            driver.DriverManager('drops.middleware', mid,
                                 invoke_on_load=True,
                                 invoke_args=[self])
