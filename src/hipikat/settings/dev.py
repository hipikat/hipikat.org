# hipikat/settings/dev.py

from inspect import currentframe, getfile
from unipath import Path
from revkom.utils import flat_list, unique_list


g = globals()


# Debugging and development modes
DEBUG = True


###
# Inherit from local base (and implicitely revkom.settings.base_debug).
execfile(Path(getfile(currentframe())).parent.child('base.py'))

# Caching
CACHE_MIDDLEWARE_KEY_PREFIX = 'hipikat-dev'
# Databases
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2'
    if 'TESTING' not in g else 'django.db.backends.sqlite3',
    'NAME': 'hipikat_dev',
    'USER': 'zeno',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '',
}}
# Security
ALLOWED_HOSTS = unique_list(flat_list(
    g.get('ALLOWED_HOSTS', []), ['evilspa.dyndns.org']))
