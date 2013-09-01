# hipikat/settings/dev.py

from runpy import run_module
import sys
from unipath import Path
from cinch import DatabasesSetting


g = globals()
S = g.setdefault


# Debugging and development modes
S('DEBUG', True)

# Include settings from this project's base settings file.
g.update(run_module('hipikat.settings.base', g))
g = globals()

# Databases
if g.get('TESTING', False):
    DATABASES = {
        'default': {
            'engine': 'sqlite3',
            'name': g['DB_DIR'].child('dev-test.db'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'hipikat_dev',
            'USER': 'zeno'
        }
    }

# Security
ALLOWED_HOSTS = g['ALLOWED_HOSTS'] + [
    'evilspa.dyndns.org',
    '.hipikat.local',
]

# Request pipeline
#import pdb; pdb.set_trace()
MIDDLEWARE_CLASSES = [
    'hipikat.middleware.DebugOuterMiddleware',
] + g['MIDDLEWARE_CLASSES'] + [
    'hipikat.middleware.DebugInnerMiddleware',
]
map(MIDDLEWARE_CLASSES.remove, [
    # Uncomment the following to disable django-debug-toolbar
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
])

# Installed apps
INSTALLED_APPS = g['INSTALLED_APPS'] + [
    'debug_toolbar'
]

