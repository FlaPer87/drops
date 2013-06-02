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
