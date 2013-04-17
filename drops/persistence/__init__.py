from drops.common import config
from drops.common import decorators
from drops.common import importutils

OPTIONS = {
    'driver': ('redis', 'Redis Driver'),
}

cfg = config.namespace('persistence').from_options(**OPTIONS)


@decorators.memoize
def get_driver(driver=None):
    driver_name = "%s.%s.Driver" % (__name__, driver or cfg.driver)
    return importutils.import_object(driver_name)
