from drops.worker import base


class Console(base.BaseWorker):

    @base.BaseWorker.methods.register
    def log(self, msg):
        print msg
