# hipikat/settings/dev.py

from inspect import currentframe, getfile

from unipath import Path


###
# Local development settings
###
# Debugging and development modes
DEBUG = True

###
# Inherit from local base (and implicitely revkom.settings.base_debug).
execfile(Path(getfile(currentframe())).parent.child('base.py'))

# Security
ALLOWED_HOSTS += ['evilspa.dyndns.org']
# Caching
CACHE_MIDDLEWARE_KEY_PREFIX = 'hipikat-dev'
# Databases
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'hipikat_dev',
    'USER': 'zeno',
    'PASSWORD': '', 
    'HOST': '127.0.0.1',
    'PORT': '', 
}}
