from smartrpyc import server

from drops import registers

class Commander(server.Server):

    def __init__(self, *args, **kwargs):
        self.register = registers.get_register()
        kwargs.setdefault("methods", self.register)
        super(Commander, self).__init__(*args, **kwargs)
