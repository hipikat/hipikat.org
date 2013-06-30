# hipikat/settings/base.py

from revkom.settings import settings_path


g = globals()


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
DEBUG = globals().get('DEBUG', False)
execfile(settings_path.child('base_prod.py' if not DEBUG else 'base_debug.py'))

###
# Django
###
# Install apps after the main application.
INSTALLED_APPS = g['INSTALLED_APPS'][0:1] + [
    # django-crispy-forms: Forms have never been this crispy.
    # http://django-crispy-forms.readthedocs.org/en/latest/
    'crispy_forms',

    # django-fluent-blogs: A basic blogging engine.
    # https://github.com/edoburu/django-fluent-blogs/
    #'fluent_blogs',

    # django-fluent-contents: The fluent_contents module offers a widget.
    # engine to display various content on a Django page.
    # https://github.com/edoburu/django-fluent-contents
    #'fluent_contents',
    #'fluent_contents.plugins.text',

    # django-wysiwyg: Converts HTML textareas into rich HTML editors.
    # https://github.com/pydanny/django-wysiwyg
    #'django_wysiwyg',

] + g['INSTALLED_APPS'][1:]
