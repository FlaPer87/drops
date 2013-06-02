from oslo.config import cfg

from drops.common import importutils


OPTIONS = [
    cfg.StrOpt('register', default='drops.registers.redis.Redis')
]

CONF = cfg.CONF
CONF.register_opts(OPTIONS)

REGISTER = None


def get_register():
    global REGISTER
    if not REGISTER:
        REGISTER = importutils.import_object(CONF.register)
    return REGISTER
