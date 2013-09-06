# hipikat/settings/base.py

from unipath import Path
from cinch import cinch_settings


g = globals()


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
ALLOWED_HOSTS = [
    '.hipikat.org',
    '.hipikat.local',
]

# Include settings from cinch.settings.[prod|debug]
g.update(cinch_settings(g))

# Caching TODO
#CACHES = CachesSetting()['default'] = {'backend': 'MemcachedCache'}

# URLs
ROOT_URLCONF = 'hipikat.urls._default'
HOSTESS_URL_PACKAGE = 'hipikat.urls'

# File discovery
STATICFILES_FINDERS = [
    'revkom.staticfiles.finders.CustomFileFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
REVKOM_STATICFILES = {
    'lib/foundation/modernizr.js': Path(
        g['LIB_DIR'], 'zurb-foundation/js/vendor/custom.modernizr.js'),
}

# Request pipeline
MIDDLEWARE_CLASSES = [
    'hostess.middleware.VirtualHostURLConfMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# Installed apps
INSTALLED_APPS = [
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
]

###
# Site settings
###
SITE_RECENT_POST_COUNT = 30
