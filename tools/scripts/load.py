from smartrpyc.client import Client

c = Client("tcp://127.0.0.1:5555")
map(c.log, ["test"]*1000)
