"""
Django settings for http://hipikat.org/, using django-configurations:
http://django-configurations.readthedocs.org/en/latest/
"""

import sys
from os.path import dirname, join
from configurations import Configuration


class Base(Configuration):

    # Metadata
    PROJECT_NAME = 'hipikat'
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    LANGUAGE_CODE = 'en-au'
    TIME_ZONE = 'Australia/Perth'
    SITE_ID = 1

    # Directory structure
    BASE_DIR = dirname(dirname(dirname(__file__)))
    LIB_DIR = join(BASE_DIR, 'lib')
    VAR_DIR = join(BASE_DIR, 'var')
    ETC_DIR = join(BASE_DIR, 'etc')
    SRC_DIR = join(BASE_DIR, 'src')
    STATICFILES_DIRS = [join(SRC_DIR, 'static')]
    TEMPLATE_DIRS = [join(SRC_DIR, 'templates')]
    DB_DIR = join(VAR_DIR, 'db')
    LOG_DIR = join(VAR_DIR, 'log')
    STATIC_ROOT = join(VAR_DIR, 'static')
    MEDIA_ROOT = join(VAR_DIR, 'media')

    # Debugging, development and testing
    TESTING = True if 'test' in sys.argv else False
    DEBUG = False
    @staticmethod
    def _setup__debug(cls):
        cls.TEMPLATE_DEBUG = cls.DEBUG

    # Databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'hipikat.org',
            'USER': 'hipikat',
        }
    }

    # Security
    ALLOWED_HOSTS = ['.hipikat.org', '.hipikat.local']
    INTERNAL_IPS = ['127.0.0.1']

    # URLs
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    # File discovery
    STATICFILES_DIRS = [join(SRC_DIR, 'static')]
    STATICFILES_FINDERS = [
        'revkom.staticfiles.finders.CustomFileFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    REVKOM_STATICFILES = {
        'lib/foundation/modernizr.js': join(
            LIB_DIR, 'zurb-foundation/js/vendor/custom.modernizr.js'),
    }

    # Request pipeline
    ROOT_HOSTCONF = 'hipikat.hosts'
    DEFAULT_HOST = 'main'
    ROOT_URLCONF = 'hipikat.urls._default'
    TEMPLATE_CONTEXT_PROCESSORS = [
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
    ]
    MIDDLEWARE_CLASSES = [
        'django_hosts.middleware.HostsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # Installed apps
    INSTALLED_APPS = [
        'hipikat',      # This project
        'revkom',       # revkom-helpers: Software patterns, utils, mixins etc

        'django_extensions',    # django-extensions: shell_plus, runserver_plus, etc.
        'crispy_forms',         # django-crispy-forms: Forms have never been this crispy
        'south',                # South: Database-agnostic migrations for Django applications

        'django_hosts',
    
        # django-fluent-pages: A polymorphic-pages-in-a-tree structure.
        'fluent_pages',
        'fluent_pages.pagetypes.flatpage',          # requires django-wysiwyg
        'fluent_pages.pagetypes.fluentpage',        # requires django-fluent-contents(?)
        'fluent_pages.pagetypes.redirectnode',      # requires django-any-urlfield
    
        # django-fluent-contents: A collection of apps to build an end-user CMS for Django admin.
        'fluent_contents',
        'fluent_contents.plugins.text',                # requires django-wysiwyg
        'fluent_contents.plugins.code',                # requires pygments
        'fluent_contents.plugins.gist',
        'fluent_contents.plugins.googledocsviewer',
        'fluent_contents.plugins.iframe',
        #'fluent_contents.plugins.markup',
        'fluent_contents.plugins.rawhtml',

        'mptt',
        'polymorphic',
        'polymorphic_tree',
    
        'django_wysiwyg',       # django-wysiwyg: Converts HTML textareas into rich HTML editors
        'any_urlfield',         # django-any-urlfield: URL selector supprting external URLs and models

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

    @classmethod
    def setup(cls):
        super(Base, cls).setup()
        for name in dir(cls):
            if name.startswith('_setup__'):
                getattr(cls, name)(cls)

    ###
    # Third-party apps
    ###

    # django-fluent-contents
    FLUENT_MARKUP_LANGUAGE = 'reStructuredText'        # can also be markdown or textile


class Debug(Base):

    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = { 
        'INTERCEPT_REDIRECTS': False,
    }
    TEMPLATE_STRING_IF_INVALID = 'INVALID_CONTEXT[%s]'

    @classmethod
    def setup(cls):
        super(Debug, cls).setup()

        if cls.TESTING:
            DATABASES = {
                'default': {
                    'engine': 'sqlite3',
                    'name': join(cls.DB_DIR, 'test-run.db'),
                }
            }

        cls.MIDDLEWARE_CLASSES = [
            'hipikat.middleware.DebugOuterMiddleware',
        ] + cls.MIDDLEWARE_CLASSES + [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'hipikat.middleware.DebugInnerMiddleware',
        ]

        cls.INSTALLED_APPS = cls.INSTALLED_APPS + [
            'debug_toolbar', 
        ]


class Default(Debug):

    # Security
    SECRET_KEY = '12345'

    @classmethod
    def setup(cls):
        super(Default, cls).setup()

        # Databases
        cls.DATABASES = { 
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': join(cls.DB_DIR, 'default.db'),
            }   
        }


class Development(Debug):
    pass


class Production(Base):
    pass
