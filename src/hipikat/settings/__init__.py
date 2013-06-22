
settings_wip = {}

def load_settings(module, wip):
    settings_wip.update(filter(lambda v: v == v.upper(), wip))
    __import__(module, level=0)
    regurn filter(globals())
