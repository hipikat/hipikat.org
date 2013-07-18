# hipikat/settings/base.py

from unipath import Path
from revkom.settings import base_settings_mixin


g = globals()

###
# Local project settings
###
# Metadata
PROJECT_NAME = 'hipikat'
PROJECT_DIR = Path(__file__).ancestor(4)
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

# Enable pre-configured apps from revkom_settings
REVKOM_INSTALL_APPS = [
    # django-crispy-forms: Forms have never been this crispy.
    # http://django-crispy-forms.readthedocs.org/en/latest/
    'crispy_forms',
    # django-wysiwyg: Converts HTML textareas into rich HTML editors.
    # https://github.com/pydanny/django-wysiwyg
    'django_wysiwyg',
    # django-fluent-contents: The fluent_contents module offers a widget.
    # engine to display various content on a Django page.
    # https://github.com/edoburu/django-fluent-contents
    #'fluent_contents',
    #'fluent_contents.plugins.code',
    #'fluent_contents.plugins.gist',
    #'fluent_contents.plugins.rawhtml',
    #'fluent_contents.plugins.text',
    # django-fluent-pages: A polymorphic page structure... content in a tree.
    # https://github.com/edoburu/django-fluent-pages
    #'fluent_pages',
    #'mptt',
    #'polymorphic',
    #'polymorphic_tree',
    #'fluent_pages.pagetypes.fluentpage',
    #'fluent_pages.pagetypes.redirectnode',
    # django-fluent-blogs: A basic blogging engine.
    # https://github.com/edoburu/django-fluent-blogs/
    #'fluent_blogs',
    #'categories',
    #'categories.editor',
    #'fluent_blogs.pagetypes.blogpage',
]

###
# Inherit default settings from a revkom settings file.
execfile(base_settings_mixin('prod' if not g.get('DEBUG') else 'debug'))
###

# Add static files from submodule libraries to known staticfiles.
REVKOM_STATICFILES = {
    'lib/foundation/modernizr.js': g['LIB_DIR'].child(
        *'zurb-foundation/js/vendor/custom.modernizr.js'.split('/')),
}
