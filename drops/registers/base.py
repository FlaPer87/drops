import logging

from smartrpyc.client import pirate
from smartrpyc.server import base

from drops.common import config


OPTIONS = {
    'worker_retries': (3, "Retries per worker"),
    'worker_timeout': (1000, 'Timeout per worker'),
}

cfg = config.namespace('registers:default').from_options(**OPTIONS)


LOG = logging.getLogger(__name__)


class RemoteMethods(base.MethodsRegister):

    def remote_store(self, name, method):
        raise NotImplementedError

    def remote_lookup(self, name):
        raise NotImplementedError

    def store(self, name, method):
        super(RemoteMethods, self).store(name, method)
        self.remote_store(name, method)

    def remotely(self, client, name):
        def method_proxy(request, *args, **kwargs):
            return getattr(client, name)(*args, **kwargs)
        return method_proxy

    def lookup(self, name):
        try:
            LOG.debug("Attempting to load local method: %s" % name)
            method = super(RemoteMethods, self).lookup(name)
        except KeyError:
            LOG.debug("Attempting to load remote method: %s" % name)
            remote = self.remote_lookup(name)
            client = pirate.Lazy(retries=cfg.worker_retries,
                                 timeout=cfg.worker_timeout,
                                 address=remote)
            method = self.remotely(client, name)
        LOG.debug("Method %s found" % method)
        return method
