from oslo.config import cfg
from smartrpyc import server
from stevedore import driver

from drops import registers


OPTIONS = [
    cfg.ListOpt('scheduler_middleware',
                default=['persistence'],
                help='Default Middlewares'),
]

CONF = cfg.CONF
CONF.register_opts(OPTIONS)


class Commander(server.Server):

    def __init__(self, *args, **kwargs):
        self.register = registers.get_register()
        kwargs.setdefault("methods", self.register)
        super(Commander, self).__init__(*args, **kwargs)

        self._load_middleware()

    def _load_middleware(self):
        for mid in CONF.scheduler_middleware:
            driver.DriverManager('drops.middleware', mid,
                                 invoke_on_load=True)
