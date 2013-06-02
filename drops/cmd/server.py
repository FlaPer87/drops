import sys

from stevedore import driver

from drops.common import config
from drops.scheduler import rpc

OPTIONS = {
    'listen': ("tcp://127.0.0.1:5555", "Default Listen"),
    'workers': ([], "Enabled workers"),
}

cfg = config.project('drops')
conf = cfg.from_options(**OPTIONS)


def fail(returncode, e):
    sys.stderr.write("ERROR: %s\n" % e)
    sys.exit(returncode)


def run():
    try:
        cfg.load(args=sys.argv[1:])

        for worker in conf.workers:
            driver.DriverManager('drops.workers', worker)

        server = rpc.Commander()
        server.bind(conf.listen)
        server.run()

    except KeyboardInterrupt:
        fail(1, '... terminating drops worker')
    except RuntimeError as e:
        fail(1, e)
