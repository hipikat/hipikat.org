"""
Django settings for http://hipikat.org/, using django-configurations.
"""

from itertools import chain
from os import path
from os.path import dirname
from cinch import BaseConfiguration, FHSDirsMixin, HostsURLsMixin
#from configurations.values import SecretValue
from configurations import values


class Base(
        # Set {LIB,VAR,ETC,SRC,DB,LOG}_DIR settings, relative to BASE_DIR
        FHSDirsMixin,
        # Setup for django-hosts, using global and debug url modules
        HostsURLsMixin,
        # Normalize settings
        BaseConfiguration):

    # TODO: Abstract configurable local site settings into a 'local settings model'(?)
    SITE_RECENT_POST_COUNT = 30

    # Metadata
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    ALLOWED_HOSTS = ['.hipikat.org']
    BASE_DIR = dirname(dirname(dirname(__file__)))
    LANGUAGE_CODE = 'en-au'
    PROJECT_NAME = 'hipikat'
    #SECRET_KEY = values.SecretValue()
    SECRET_KEY = values.Value('12345')
    TIME_ZONE = 'Australia/Perth'

    class CinchMeta(object):
        """django-cinch simplifies some core configuration."""
        # Databases
        DATABASE_TYPE = 'postgresql'
        DATABASE_NAME = 'hipikat_prod'

        # Logging (TODO: implement)
        LOGGING_SETUP = 'filesystem'
        LOGFILE_BACKUPS = 2

    # File discovery
    STATICFILES_FINDERS = [
        #'revkom.staticfiles.finders.CustomFileFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    @classmethod
    def _setup__staticfiles_dirs(cls):
        cls.STATICFILES_DIRS = [
            path.join(cls.SRC_DIR, 'static'),
            ('zurb', path.join(cls.LIB_DIR, 'zurb-foundation', 'js')),
        ]

    # TODO: Add this to documentation somewhere before deleting it since it's
    # currently the only actual use of the CustomFileFinder staticfile finder.
    #@classmethod
    #def _setup__revkom_staticfiles(cls):
    #    cls.REVKOM_STATICFILES_CUSTOM = {
    #        'lib/foundation/modernizr.js': path.join(
    #            cls.LIB_DIR, 'zurb-foundation/js/vendor/custom.modernizr.js'),
    #        'lib/foundation/foundation.js': path.join(
    #            cls.LIB_DIR, 'zurb-foundation/js/foundation/foundation.js'),
    #    }

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
    INSTALLED_APPS = [
        'hipikat',              # This project
        'revkom',               # revkom-helpers: Software patterns, utils, mixins etc

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
        'fluent_contents.plugins.markup',   # this was commented out? breaks something?
        'fluent_contents.plugins.rawhtml',

        # django-fluent-blogs
        'fluent_blogs',

        # Required by django-fluent apps
        'mptt',
        'polymorphic',
        'polymorphic_tree',
        'categories',
        'categories.editor',
        'taggit',
        'taggit_autocomplete_modified',
        'django_wysiwyg',       # django-wysiwyg: Converts HTML textareas into rich HTML editors
        'any_urlfield',         # django-any-urlfield: URL selector for external URLs and models
    ]
    # Separate out contrib apps for the 'Core' configuration; see below.
    installed_django_contrib_apps = ['django.contrib.' + dj_app for dj_app in
                                     ('admin', 'admindocs', 'auth', 'contenttypes', 'humanize',
                                      'messages', 'sessions', 'staticfiles', 'sites')]
    INSTALLED_APPS += installed_django_contrib_apps

    ###
    # Third-party app settings
    ###

    # The Fluent suite
    @classmethod
    def _setup__fluent(cls):
        cls.FLUENT_PAGES_TEMPLATE_DIR = path.join(cls.SRC_DIR, 'layouts')
        cls.FLUENT_PAGES_BASE_TEMPLATE = 'base-fluent.html'

    # django-fluent-contents
    FLUENT_MARKUP_LANGUAGE = 'reStructuredText'        # can also be markdown or textile

    # django-wysiwyg
    DJANGO_WYSIWYG_FLAVOR = "yui_advanced"


class Debug(Base):
    """
    Configuration for debugging. This class attempts to remain close to
    a production profile, while just switching on more debugging features
    and increasing logging. For development, use Development.
    """

    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    TEMPLATE_STRING_IF_INVALID = 'INVALID_CONTEXT<%s>'

    @classmethod
    def setup(cls):
        super(Debug, cls).setup()

        # Use an sqlite database during testing to increase test speeds
        if cls.TESTING:
            cls.DATABASES['default'] = {
                'engine': 'sqlite3',
                'name': path.join(cls.DB_DIR, 'test-run.db'),
            }

        # Request pipeline
        cls.MIDDLEWARE_CLASSES = tuple(chain([
            'hipikat.middleware.debug.DebugOuterMiddleware',
        ], cls.MIDDLEWARE_CLASSES, [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'hipikat.middleware.debug.DebugInnerMiddleware',
        ]))

        # Installed apps
        cls.INSTALLED_APPS = tuple(chain(
            cls.INSTALLED_APPS,
            ['debug_toolbar']
        ))


class Core(Base):
    """
    A configuration which reduces ``INSTALLED_APPS`` to a core set of apps,
    used for (inital) ``manage.py syncdb`` calls on blank databases... because
    sometimes third-party apps have a dependance on the content_types table
    having already been created. (I'm looking at you, django-fluent family.)
    """
    INSTALLED_APPS = ['south'] + Base.installed_django_contrib_apps


class Default(Debug):
    pass
    # Security
    #SECRET_KEY = '12345'

    #@classmethod
    #def setup(cls):
    #    super(Default, cls).setup()

    #    # Databases
    #    cls.DATABASES = {
    #        'default': {
    #            'ENGINE': 'django.db.backends.sqlite3',
    #            'NAME': path.join(cls.DB_DIR, 'default.db'),
    #        }
    #    }


class Development(Debug):
    pass


class Production(Base):
    pass
