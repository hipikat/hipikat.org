# hipikat/settings/base.py

from revkom.settings import settings_path


###
# Local project settings
###
# Metadata
PROJECT_NAME = 'hipikat'
ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'
# Security
ALLOWED_HOSTS = ['.hipikat.org']
# Caching
CACHE_MIDDLEWARE_KEY_PREFIX = 'hipikat'
CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
    'TIMEOUT': 60,
}}

###
# Inherit from a fine set of default settings. (Note: this also sets g and s.)
DEBUG = False if 'DEBUG' not in globals() else DEBUG
execfile(settings_path.child('base_prod.py' if not DEBUG else 'base_debug.py'))

###
# Django
###
# Install apps after the main application.
INSTALLED_APPS = INSTALLED_APPS[0:1] + [
    # django-crispy-forms: Forms have never been this crispy.
    # http://django-crispy-forms.readthedocs.org/en/latest/
    'crispy_forms',
] + INSTALLED_APPS[1:]
