"""
Django settings for http://hipikat.org/, using django-configurations.
"""

from os import environ
from os.path import dirname, join
from configurations import Configuration
from cinch.configurations import (BaseConfiguration, EnvdirMixin, FHSDirsMixin,
    HostsURLsMixin)


class LocalSiteBase(EnvSettingsMixin, FHSDirsMixin, HostsURLsMixin,
    BaseConfiguration):

    # Metadata
    ADMINS = (
        ('Adam Wright', 'adam@hipikat.org'),
    )
    ALLOWED_HOSTS = ['.hipikat.org']
    BASE_DIR = dirname(dirname(dirname(__file__)))
    LANGUAGE_CODE = 'en-au'
    PROJECT_NAME = 'hipikat'
    TIME_ZONE = 'Australia/Perth'

    # EnvSettingsMixin
    ENV_SETTINGS = ['SECRET_KEY']

    # File discovery
    STATICFILES_FINDERS = [
        'revkom.staticfiles.finders.CustomFileFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]  

    # Site-specific settings
    SITE_RECENT_POST_COUNT = 30

    ###
    # Third-party app settings
    ###

    # Revkom - Adam Wright's in vitro shared code base...
    REVKOM_STATICFILES = {
        'lib/foundation/modernizr.js': join(
            LIB_DIR, 'zurb-foundation/js/vendor/custom.modernizr.js'),
        'lib/foundation/foundation.js': join(
            LIB_DIR, 'zurb-foundation/js/foundation/foundation.js'),
    }

    # The Fluent suite
    @classmethod
    def setup__fluent(cls):
        FLUENT_PAGES_TEMPLATE_DIR = join(cls.SRC_DIR, 'layouts')
        FLUENT_PAGES_BASE_TEMPLATE = 'base-fluent.html'


class Base(LocalSiteMixin, Configuration):

    #FLUENT_BLOGS_BASE_TEMPLATE
    TEMPLATE_DIRS = [
        join(SRC_DIR, 'templates'),
        FLUENT_PAGES_TEMPLATE_DIR,
    ]

    # Request pipeline
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
    @staticmethod
    def _setup__intalled_apps(cls):
        cls.INSTALLED_APPS = [
            cls.PROJECT_NAME,   # This project
    
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
    
            # django-fluent-blogs
            'fluent_blogs',
    
            'mptt',
            'polymorphic',
            'polymorphic_tree',
            'categories',
            'categories.editor',
            'taggit',
            'taggit_autocomplete_modified',
            'django_wysiwyg',       # django-wysiwyg: Converts HTML textareas into rich HTML editors
            'any_urlfield',         # django-any-urlfield: URL selector supprting external URLs and models
        ]

    ###
    # Third-party apps
    ###

    # django-fluent-contents
    FLUENT_MARKUP_LANGUAGE = 'reStructuredText'        # can also be markdown or textile

    # django-wysiwyg
    DJANGO_WYSIWYG_FLAVOR = "yui_advanced"


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

