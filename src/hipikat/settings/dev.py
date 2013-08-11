# hipikat/settings/dev.py

from runpy import run_module
import sys
from unipath import Path
from cinch import DatabasesSetting


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', True)

# Include settings from this project's base settings file.
G.update(run_module('hipikat.settings.base', G))

# Databases
if G.get('TESTING', False):
    DATABASES = DatabasesSetting()['default'] = {
        'engine': 'sqlite3',
        'name': G['DB_DIR'].child('dev-test.db'),
    }
else:
    DATABASES = DatabasesSetting()['default'] = {
        'engine': 'postgresql',
        'name': 'hipikat_dev',
        'user': 'zeno'
    }

# Security
G['ALLOWED_HOSTS'].append('evilspa.dyndns.org')

# Request pipeline
MIDDLEWARE_CLASSES = [
    'hipikat.middleware.DebugOuterMiddleware',
] + G['MIDDLEWARE_CLASSES'] + [
    'hipikat.middleware.DebugInnerMiddleware',
]
map(MIDDLEWARE_CLASSES.remove, [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    ])
