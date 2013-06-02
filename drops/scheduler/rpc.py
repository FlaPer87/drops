from smartrpyc import server
from stevedore import driver

from drops.common import config
from drops import registers


OPTIONS = {
    'scheduler_middleware': (['persistence'], 'Default Middlewares'),
}

conf = config.project("drops")
prj = conf.from_options(**OPTIONS)


class Commander(server.Server):

    def __init__(self, *args, **kwargs):
        self.register = registers.get_register()
        kwargs.setdefault("methods", self.register)
        super(Commander, self).__init__(*args, **kwargs)

        self._load_middleware()

    def _load_middleware(self):
        for mid in prj.scheduler_middleware:
            driver.DriverManager('drops.middleware', mid,
                                 invoke_on_load=True)
