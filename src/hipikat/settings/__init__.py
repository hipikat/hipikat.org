
from inspect import currentframe, getfile
from unipath import Path


__all__ = ['settings_path', 'settings_macros',]


settings_path = Path(getfile(currentframe())).parent

def settings_macros():
    return settings_path.child('_macros.py')
