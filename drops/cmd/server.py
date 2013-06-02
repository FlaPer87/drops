import sys

from oslo.config import cfg
from stevedore import driver

from drops.scheduler import rpc

OPTIONS = [
    cfg.StrOpt('listen',
               default='tcp://127.0.0.1:5555',
               help="Default Listen"),
    cfg.ListOpt('workers', default=[],
               help="Default Listen")
]

CONF = cfg.CONF
CONF.register_cli_opts(OPTIONS)


def fail(returncode, e):
    sys.stderr.write("ERROR: %s\n" % e)
    sys.exit(returncode)


def run():
    try:
        CONF(args=sys.argv[1:])

        for worker in CONF.workers:
            driver.DriverManager('drops.workers', worker)

        server = rpc.Commander()
        server.bind(CONF.listen)
        server.run()

    except KeyboardInterrupt:
        fail(1, '... terminating drops worker')
    except RuntimeError as e:
        fail(1, e)
