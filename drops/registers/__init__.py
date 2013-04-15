from drops.common import config, importutils


OPTIONS = {
    'register': 'drops.registers.redis.Redis',
}

cfg = config.project('drops').from_options(**OPTIONS)

REGISTER = None


def get_register():
    global REGISTER
    if not REGISTER:
        REGISTER = importutils.import_object(cfg.register)
    return REGISTER
