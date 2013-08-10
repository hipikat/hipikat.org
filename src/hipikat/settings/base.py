# hipikat/settings/base.py

from unipath import Path
from cinch.settings import base_settings_mixin, cache_setting


G = globals()
S = G.setdefault


###
# Local project settings
###
# Metadata
PROJECT_DIR = Path(__file__).ancestor(4)
PROJECT_NAME = 'hipikat'
ADMINS = [('Adam Wright', 'adam@hipikat.org')]
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'

# Caching
S('CACHE_MIDDLEWARE_KEY_PREFIX', 'hipikat')

# Include default settings from a django-cinch settings file.
execfile(base_settings_mixin('prod' if not G.get('DEBUG') else 'debug'))

# Security
G['ALLOWED_HOSTS'].append('.hipikat.org')

# Caching
G['CACHES']['default'] = cache_setting(backend='memcached', timeout=60)

# File discovery
G['TEMPLATE_LOADERS'].prepend('revkom.staticfiles.finders.CustomFileFinder')
S('REVKOM_STATICFILES', {
    # Add static files from submodule libraries to discoverable staticfiles.
    'lib/foundation/modernizr.js': Path(
        G['LIB_DIR'], 'zurb-foundation/js/vendor/custom.modernizr.js'),
})

# Request pipeline
G['MIDDLEWARE_CLASSES'].prepend(
    'hostess.middleware.VirtualHostURLConfMiddleware'
).append(
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

# Installed apps
G['INSTALLED_APPS'].prepend(
    # djagno-hostess: Virtual host and subdomain processing
    # http://github.com/hipikat/django-hostess
    'hostess',
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
)

# django-sassmouth (NB: this project is on hold; settings not currently used)
SASSMOUTH_DEBUG = G['DEBUG']
SASSMOUTH_COMPRESS = not G['DEBUG']
SASSMOUTH_BUILD_DIR = G['TMP_DIR'].child('_build_sassyfiles')
SASSMOUTH_SEARCH_PATHS = [
    Path(G['LIB_DIR'], 'zurb-foundation/scss/'),
    Path(G['LIB_DIR'], 'compass/frameworkds/compass/stylesheets/'),
]
SASSMOUTH_TARGETS = {
    'stylesheets/hipikat.css': {
        'src': Path(G['SRC_DIR'], 'sass/hipikat.scss'),
    }
}

###
# Site settings
###
SITE_RECENT_POST_COUNT = 30
