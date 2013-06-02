from oslo.config import cfg
from stevedore import driver


OPTIONS = [
    cfg.StrOpt('driver', default='redis',
               help='Redis Driver'),
]

cfg.CONF.register_opts(OPTIONS)


def get_driver(conf, backend=None):
    instance = driver.DriverManager('drops.persistence',
                                    backend or conf.driver,
                                    invoke_on_load=True,
                                    invoke_args=[conf])
    return instance.driver
