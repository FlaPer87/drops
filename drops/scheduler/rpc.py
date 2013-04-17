from smartrpyc import server

from drops.common import config
from drops.common import importutils
from drops import registers


def _prepend(name):
    return "drops.scheduler.middleware.%s" % name

OPTIONS = {
    'scheduler_middleware': ([_prepend('persistence.PersistenceMiddleware')],
                             'Default Middlewares'),
}

prj = config.project("drops").from_options(**OPTIONS)


class Commander(server.Server):

    def __init__(self, *args, **kwargs):
        self.register = registers.get_register()
        kwargs.setdefault("methods", self.register)
        super(Commander, self).__init__(*args, **kwargs)

        self._load_middleware()

    def _load_middleware(self):
        for mid in prj.scheduler_middleware:
            try:
                self.middleware.append(importutils.import_object(mid))
            except ImportError as exc:
                print exc
