from smartrpyc import client
from smartrpyc.server import base

from drops import persistence as db


class PersistenceMiddleware(base.ServerMiddlewareBase):

    def __init__(self, *args, **kwargs):
        super(PersistenceMiddleware, self).__init__(*args, **kwargs)
        self.driver = db.get_driver()

    def pre(self, request, method):
        status = "taken"
        try:
            cls = method.__class__
            if isinstance(cls, client.Client):
                status = "received"
        except AttributeError:
            pass

        raw = request.raw
        tid = raw.setdefault("k", {}).setdefault("tid", request.id)
        msg = {
            "status": status,
            "msg": request.raw,
        }
        self.driver.upsert("message", tid, **msg)
