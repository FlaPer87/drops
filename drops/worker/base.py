from drops import registers


class BaseWorker(object):

    # Gest default register and sets it
    # as class attribute
    methods = registers.get_register()
