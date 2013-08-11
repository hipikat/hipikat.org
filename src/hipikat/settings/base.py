# hipikat/settings/base.py

from runpy import run_module
from unipath import Path
from cinch import CachesSetting, SettingList, cinch_settings


G = globals()


###
# Local project settings
###
# Metadata
PROJECT_DIR = Path(__file__).ancestor(4)
PROJECT_NAME = 'hipikat'
ADMINS = [('Adam Wright', 'adam@hipikat.org')]
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'

# Security
ALLOWED_HOSTS = ['.hipikat.org']

# Include settings from cinch.settings.[prod|debug]
G.update(cinch_settings(G))

# Caching
CACHES = CachesSetting()['default'] = {'backend': 'MemcachedCache'}

# File discovery
TEMPLATE_LOADERS = SettingList(
    'revkom.staticfiles.finders.CustomFileFinder'
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
REVKOM_STATICFILES = {
    'lib/foundation/modernizr.js': Path(
        G['LIB_DIR'], 'zurb-foundation/js/vendor/custom.modernizr.js'),
}

# Request pipeline
MIDDLEWARE_CLASSES = SettingList(
    'hostess.middleware.VirtualHostURLConfMiddleware'
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

# Installed apps
INSTALLED_APPS = SettingList(
    'hipikat',      # This project
    'revkom',       # revkom-helpers: Software patterns, utils, mixins etc
    'hostess',      # djagno-hostess: Virtual host and subdomain processing

    'django_extensions',    # django-extensions: shell_plus, runserver_plus, etc.
    'crispy_forms',         # django-crispy-forms: Forms have never been this crispy
    'django_wysiwyg',       # django-wysiwyg: Converts HTML textareas into rich HTML editors
    'south',                # South: Database-agnostic migrations for Django applications

    # django-fluent-contents: Display various content on a Django page with widgets.
    #'fluent_contents',
    #'fluent_contents.plugins.code',
    #'fluent_contents.plugins.gist',
    #'fluent_contents.plugins.rawhtml',
    #'fluent_contents.plugins.text',

    # django-fluent-pages: A polymorphic-pages-in-a-tree structure.
    #'fluent_pages',
    #'mptt',
    #'polymorphic',
    #'polymorphic_tree',
    #'fluent_pages.pagetypes.fluentpage',
    #'fluent_pages.pagetypes.redirectnode',

    # django-fluent-blogs: A basic blogging engine.
    #'fluent_blogs',
    #'categories',
    #'categories.editor',
    #'fluent_blogs.pagetypes.blogpage',

    # Django contrib packages - https://docs.djangoproject.com/en/dev/ref/contrib/
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
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
