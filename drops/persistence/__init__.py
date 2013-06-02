from oslo.config import cfg

from drops.common import decorators
from drops.common import importutils

OPTIONS = [
    cfg.StrOpt('driver', default='redis',
               help='Redis Driver'),
]

CONF = cfg.CONF
CONF.register_opts(OPTIONS)


@decorators.memoize
def get_driver(driver=None):
    driver_name = "%s.%s.Driver" % (__name__, driver or CONF.driver)
    return importutils.import_object(driver_name)
