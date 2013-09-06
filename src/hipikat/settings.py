"""
Django settings for http://hipikat.org/, using django-configurations.
"""

from os import environ
from os.path import dirname, join
import sys
from configurations import Configuration


class LocalSiteMixin(object):
    # Metadata
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    LANGUAGE_CODE = 'en-au'
    TIME_ZONE = 'Australia/Perth'

    # Site-specific settings
    SITE_RECENT_POST_COUNT = 30


class Base(LocalSiteMixin, Configuration):

    PROJECT_NAME = 'hipikat'
    SITE_ID = 1
    USE_I18N = False    # Internationalisation framework
    USE_L10N = True     # Localisation framework
    USE_TZ = True       # Timezone support for dates

    # Directory structure
    BASE_DIR = dirname(dirname(dirname(__file__)))
    LIB_DIR = join(BASE_DIR, 'lib')
    VAR_DIR = join(BASE_DIR, 'var')
    ETC_DIR = join(BASE_DIR, 'etc')
    SRC_DIR = join(BASE_DIR, 'src')
    DB_DIR = join(VAR_DIR, 'db')
    LOG_DIR = join(VAR_DIR, 'log')
    #sys.path.insert(0, join(SRC_DIR, 'apps'))

    # Debugging, development and testing
    TESTING = True if 'test' in sys.argv else False
    DEBUG = False
    @staticmethod
    def _setup__debug(cls):
        cls.TEMPLATE_DEBUG = cls.DEBUG
        cls.DEBUG_URL_PATTERNS = cls.DEBUG

    # Databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'hipikat_dev',
            'USER': 'zeno',
        }
    }
    #DATABASES = { 
    #    'default': {
    #        'engine': 'sqlite3',
    #        'name': join(DB_DIR, 'base.db'),
    #    }   
    #} 

    # Security
    ALLOWED_HOSTS = ['.hipikat.org', '.hipikat.local']
    INTERNAL_IPS = ['127.0.0.1']
    SECRET_KEY_FILE = join(VAR_DIR, 'env/SECRET_KEY')
    SECRET_KEY = environ['SECRET_KEY']

    # URLs
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    # File discovery
    MEDIA_ROOT = join(VAR_DIR, 'media')
    STATIC_ROOT = join(VAR_DIR, 'static')
    STATICFILES_DIRS = [join(SRC_DIR, 'static')]
    STATICFILES_FINDERS = [
        'revkom.staticfiles.finders.CustomFileFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    REVKOM_STATICFILES = {
        'lib/foundation/modernizr.js': join(
            LIB_DIR, 'zurb-foundation/js/vendor/custom.modernizr.js'),
        'lib/foundation/foundation.js': join(
            LIB_DIR, 'zurb-foundation/js/foundation/foundation.js'),
    }
    FLUENT_PAGES_TEMPLATE_DIR = join(SRC_DIR, 'layouts')
    FLUENT_PAGES_BASE_TEMPLATE = 'base-fluent.html'
    TEMPLATE_DIRS = [
        join(SRC_DIR, 'templates'),
        FLUENT_PAGES_TEMPLATE_DIR,
    ]

    # Request pipeline
    ROOT_HOSTCONF = PROJECT_NAME + '.hosts'
    DEFAULT_HOST = 'main'
    ROOT_URLCONF = PROJECT_NAME + '.urls._default'
    MIDDLEWARE_CLASSES = [
        'django_hosts.middleware.HostsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        'hipikat.styles.context_processor',
    ]

    # Installed apps
    INSTALLED_APPS = [
        PROJECT_NAME,   # This project

        'revkom',       # revkom-helpers: Software patterns, utils, mixins etc

        'django_extensions',    # django-extensions: shell_plus, runserver_plus, etc.
        'crispy_forms',         # django-crispy-forms: Forms have never been this crispy
        'south',                # South: Database-agnostic migrations for Django applications

        'django_hosts',
    
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


class Core(Base):
    """
    A configuration which reduces ``INSTALLED_APPS`` to a core set of apps,
    used for (inital) ``manage.py syncdb`` calls on blank databases,
    beacuse sometimes third-party apps have a dependance on a content_types
    table already having been created.
    """
    INSTALLED_APPS = ['south'] + ['djang.contrib.' + dj_app
        for dj_app in ('admin', 'admindocs', 'auth', 'contenttypes', 'humanize',
                       'messages', 'sessions', 'staticfiles', 'sites')]


class Development(Debug):
    pass


class Production(Base):
    pass

