# hipikat/settings/dev.py

from inspect import currentframe, getfile
from functools import partial
from unipath import Path


g = globals()


# Debugging and development modes
DEBUG = True


###
# Inherit from local base (and implicitely revkom.settings.base_debug).
execfile(Path(getfile(currentframe())).parent.child('base.py'))
###


# Directory structure
DEV_DIR = g['PROJECT_DIR'].child('dev')

# Caching
CACHE_MIDDLEWARE_KEY_PREFIX = 'hipikat-dev'

# Databases
if g.get('TESTING', False):
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': g['DB_DIR'].child('dev-test.db')
    }}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hipikat_dev',
        'USER': 'zeno',
        'HOST': '127.0.0.1',
    }}

# Security
G('ALLOWED_HOSTS').add('evilspa.dyndns.org')
#ALLOWED_HOSTS.
#    g.get('ALLOWED_HOSTS'), ['evilspa.dyndns.org'])

# Middleware
middleware = g['MIDDLEWARE_CLASSES']
prepend_middleware = [
    'hipikat.middleware.DebugOuterMiddleware',
]
append_middleware = [
    'hipikat.middleware.DebugInnerMiddleware',
]
remove_middleware = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
]
map(partial(middleware.insert, 0), prepend_middleware)
map(middleware.append, append_middleware)
map(middleware.remove, remove_middleware)
