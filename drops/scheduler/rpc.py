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
        self.register = registers.get_register()
        kwargs.setdefault("methods", self.register)
        super(Commander, self).__init__(*args, **kwargs)

        self._load_middleware()

    def bind(self):
        super(Commander, self).bind(self.conf.listen)

    def _load_middleware(self):
        for mid in self.conf.scheduler_middleware:
            driver.DriverManager('drops.middleware', mid,
                                 invoke_on_load=True,
                                 invoke_args=[self])
