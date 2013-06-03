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

import sys

from oslo.config import cfg
from stevedore import driver

from drops.scheduler import rpc

OPTIONS = [
    cfg.StrOpt('listen',
               default='tcp://127.0.0.1:5555',
               help="Default Listen"),
    cfg.ListOpt('workers', default=[],
               help="Default Listen")
]

CONF = cfg.CONF
CONF.register_cli_opts(OPTIONS)


def fail(returncode, e):
    sys.stderr.write("ERROR: %s\n" % e)
    sys.exit(returncode)


def run():
    try:
        CONF(args=sys.argv[1:])

        server = rpc.Commander(CONF)

        for worker in CONF.workers:
            worker = driver.DriverManager('drops.workers',
                                          worker,
                                          invoke_on_load=True,
                                          invoke_args=[CONF])
            server.add_worker(worker.driver)

        server.bind()
        server.run()
    except KeyboardInterrupt:
        fail(1, '... terminating drops worker')
    except RuntimeError as e:
        fail(1, e)
