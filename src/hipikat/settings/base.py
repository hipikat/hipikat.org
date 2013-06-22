###
# Copyright (C) 2013 Adam Wright <adam@hipikat.org>
#
# Base settings for the Hipikat site. These are configuration defaults
# which act like an abstract base class for settings files; they do not,
# in and of themselves, form a working project's worth of settings.
#
# https://docs.djangoproject.com/en/dev/topics/settings/
###

from inspect import currentframe, getfile
import sys
from django.core.exceptions import ImproperlyConfigured
from unipath import Path
from .common import project_settings


# Load settings already defined by modules importing this one.
globals().update(project_settings)
# Set a module-level attribute (global) only if it hasn't yet been set. If
# only an attribute name is given, return its value, or False if it's unset.
s = lambda k, *v: globals().setdefault(k, v[0]) \
        if len(v) else globals().get(k, False)


###
# Metadata
###
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-au'
if s('ADMINS') and not s('MANAGERS'):
    MANAGERS = ADMINS

###
# Diretory structure
###
s('PROJECT_DIR', Path(getfile(currentframe())).ancestor(4))
s('VAR_DIR', PROJECT_DIR.child('var'))
s('SRC_DIR', PROJECT_DIR.child('src'))
s('CONF_DIR', PROJECT_DIR.child('conf'))
s('TMP_DIR', VAR_DIR.child('tmp'))
# var/
s('DB_DIR', VAR_DIR.child('db'))
s('FIXTURE_DIRS', (VAR_DIR.child('fixtures'),))
s('LOG_DIR', VAR_DIR.child('log'))
s('STATICFILES_DIRS', (VAR_DIR.child('static'),))
s('MEDIA_ROOT', TMP_DIR.child('media'))         # Set to var/media in base_prod
# src/
s('TEMPLATE_DIRS', (SRC_DIR.child('templates'),))
# Add src/apps/ to the front of the Python path
sys.path.insert(0, SRC_DIR.child('apps'))

###
# Security
###
# By default we look for a secret key in conf/SECRET_KEY. New secret keys
# can be generated with the command: manage.py make_secret_key
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
s('SECRET_KEY_FILE', CONF_DIR.child('SECRET_KEY'))
if not s('SECRET_KEY') and s('SECRET_KEY_FILE').exists():
    SECRET_KEY = s('SECRET_KEY_FILE').read_file()

###
# Logging and debugging
###
s('DEBUG', False)
s('TEMPLATE_DEBUG', False)





DATABASES = {'default': {}}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hipikat.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hipikat.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'hipikat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Limit attributes seen by imports to actual settings
__all__ = [setting for setting in dir() if setting.upper() == setting]

