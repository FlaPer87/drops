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

from oslo.config import cfg
from stevedore import driver


OPTIONS = [
    cfg.StrOpt('register', default='redis')
]

CONF = cfg.CONF
CONF.register_opts(OPTIONS)


def get_register(conf=None):
    register = CONF.register

    if conf:
        register = conf.register

    instance = driver.DriverManager('drops.registers', register,
                                    invoke_on_load=True,
                                    invoke_args=[conf or CONF])
    return instance.driver
