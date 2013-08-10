# hipikat/settings/dev.py

from inspect import currentframe, getfile
from unipath import Path
from cinch import db_setting


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', True)

# Caching
S('CACHE_MIDDLEWARE_KEY_PREFIX', 'hipikat-dev')

# Include settings from this project's base settings file.
execfile(Path(getfile(currentframe())).parent.child('base.py'))

# Directory structure
S('DEV_DIR', G['PROJECT_DIR'].child('dev'))

# Databases
if G.get('TESTING', False):
    G['DATABASES']['default'] = db_setting(engine='sqlite3',
                                           name=G['DB_DIR'].child('dev-test.db'))
else:
    G['DATABASES']['default'] = db_setting(engine='postgresql',
                                           name='hipikat_dev',
                                           user='zeno')

# Security
G['ALLOWED_HOSTS'].append('evilspa.dyndns.org')

# Middleware
G['MIDDLEWARE_CLASSES'].prepend(
    'hipikat.middleware.DebugOuterMiddleware',
).append(
    'hipikat.middleware.DebugInnerMiddleware',
).remove(
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
