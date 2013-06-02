#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from smartrpyc import client
from smartrpyc.server import middleware

from drops import persistence as db


class PersistenceMiddleware(middleware.ServerMiddlewareBase):

    def __init__(self, scheduler, *args, **kwargs):
        super(PersistenceMiddleware, self).__init__(*args, **kwargs)
        self.scheduler = scheduler
        self.driver = db.get_driver(self.scheduler.conf)

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
