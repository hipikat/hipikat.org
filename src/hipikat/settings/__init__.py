"""
Settings for the Django project on http://hipikat.org/.
"""

from itertools import chain
from os import getenv, path
from os.path import dirname
from cinch import cinch_django_settings, CinchSettings, NormaliseSettings
from cinch.mixins import FHSDirsMixin
from .logging import FileLoggingMixin


class LocalSiteSettings(object):
    """
    TODO: Abstract configurable local site settings into a 'local settings model'(?)
    """
    SITE_RECENT_POST_COUNT = 30


class Base(
        # Set {LIB,VAR,ETC,SRC,DB,LOG}_DIR settings, relative to BASE_DIR
        FHSDirsMixin,
        # Normalise settings to sensible defaults, add some conveniences
        NormaliseSettings,
        # Hard-coded (bad!) settings specific to hipikat.org
        LocalSiteSettings,
        # Basic file logging, to var/log/, with rotating 5M files (or thereabouts).
        FileLoggingMixin,
        # Base class for a django-cinch settings class
        CinchSettings):

    ### Project metadata
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    ALLOWED_HOSTS = ['.hipikat.org']
    BASE_DIR = dirname(dirname(dirname(dirname(__file__))))     # [repo]/src/[proj]/settings/[me]
    LANGUAGE_CODE = 'en-au'
    PROJECT_MODULE = 'hipikat'
    SECRET_KEY = getenv('DJANGO_SECRET_KEY')
    TIME_ZONE = 'Australia/Perth'

    ### Private project settings
    # Settings variables injected into context
    _CONTEXT_SETTINGS_VARIABLES = [
        'PROJECT_MODULE',
    ]
    # Prevent linking to javascripts (etc.) in CDNs, for offline development
    _LOCAL_SOURCES = False

    ### Debug
    DEBUG = False
    _DEBUG_TOOLBAR_ENABLED = False
    _MINIFY_RESOURCES = True

    ### Data stores
    DATABASES = {
        'default': {
            'USER': 'hipikat',
            'NAME': 'hipikat.org',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
        }
    }

    ### Request pipeline
    MIDDLEWARE_CLASSES = [
        #PROJECT_MODULE + '.style.ResourceRegistryMiddleware',
        'django_hosts.middleware.HostsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        #PROJECT_MODULE + '.style.CleanHTMLMiddleware',
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
        PROJECT_MODULE + '.context_processor',
    ]
    ROOT_URLCONF = PROJECT_MODULE + '.urls'

    # django-hosts
    ROOT_HOSTCONF = PROJECT_MODULE + '.hosts'
    DEFAULT_HOST = 'main_site'

    ### Installed apps
    INSTALLED_APPS = [
        PROJECT_MODULE,          # This project

        'revkom',               # revkom-helpers: Software patterns, utils, mixins etc

        'south',                # South: Database-agnostic migrations for Django applications
        'django_extensions',    # django-extensions: shell_plus, runserver_plus, etc.
        'django_hosts',         # django-hosts: Routes to urlconfs based on the requested domain
        'mptt',                 # django-mptt: Modified pre-order traversal trees

        'feincms', 'feincms.module.page', 'feincms.module.medialibrary',

        #'crispy_forms',         # django-crispy-forms: Forms have never been this crispy

        # Django contrib apps
        'django.contrib.admin', 'django.contrib.admindocs', 'django.contrib.auth',
        'django.contrib.contenttypes', 'django.contrib.humanize', 'django.contrib.messages',
        'django.contrib.sessions', 'django.contrib.staticfiles', 'django.contrib.sites',
    ]

    def setup(self):
        """Configure settings which require initialised base classes/mixins."""
        super(Base, self).setup()

        ### Debugging, testing, development
        self.setdefault('_DEBUG_URLPATTERNS_ENABLED', self.DEBUG)

        ### Static files
        self.STATICFILES_DIRS = [
            path.join(self.SRC_DIR, 'static'),
            ('jquery', path.join(self.LIB_DIR, 'jquery-1.10.2')),
            ('tinymce', path.join(self.LIB_DIR, 'tinymce-4.0.10', 'js', 'tinymce')),
            ('zepto', path.join(self.LIB_DIR, 'zepto-1.0')),
            ('zurb', path.join(self.LIB_DIR, 'zurb-foundation', 'js')),
            ('font-awesome', path.join(self.LIB_DIR, 'Font-Awesome')),
        ]

        self.FEINCMS_RICHTEXT_INIT_CONTEXT = {
            'TINYMCE_JS_URL': self.STATIC_URL + 'tinymce/tinymce.min.js',
        }

    ### Third-party apps
    # Fluent apps
    #FLUENT_MARKUP_LANGUAGE = 'reStructuredText'     # Can also be markdown or textile

    # Miscellaneous...
    DJANGO_WYSIWYG_FLAVOR = "yui_advanced"


class Debug(Base):
    """
    Settings for debugging. This class attempts to remain close to a
    production profile, while switching on more debugging features and
    increasing logging output. For development, use Development.
    """
    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = {
        # Display a page describing redirects generated by Django,
        # rather than sending the redirect to the browser
        'INTERCEPT_REDIRECTS': False,
    }
    TEMPLATE_STRING_IF_INVALID = 'INVALID_CONTEXT<%s>'

    _DEBUG_TOOLBAR_ENABLED = True
    _MINIFY_RESOURCES = False

    def setup(self):
        super(Debug, self).setup()

        # If tests are being run (added by NormaliseSettings)
        if self.TESTING and False:
            # Use an sqlite database while testing to violently increase test speed
            self.DATABASES['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': path.join(self.DB_DIR, 'test-run.db'),
            }

        # Enable Django Debug Toolbar
        if self._DEBUG_TOOLBAR_ENABLED:
            self.MIDDLEWARE_CLASSES = tuple(chain(
                list(self.MIDDLEWARE_CLASSES),
                ['debug_toolbar.middleware.DebugToolbarMiddleware']))
            self.INSTALLED_APPS = list(chain(
                self.INSTALLED_APPS,
                ['debug_toolbar']
            ))

        # Request pipeline
        self.MIDDLEWARE_CLASSES = tuple(chain([
            self.PROJECT_MODULE + '.middleware.debug.DebugOuterMiddleware',
        ], self.MIDDLEWARE_CLASSES, [
            self.PROJECT_MODULE + '.middleware.debug.DebugInnerMiddleware',
        ]))


class Core(Base):
    """
    Settings which reduce ``INSTALLED_APPS`` to a core set of apps, used for
    inital ``manage.py syncdb`` calls on blank databases, because sometimes
    third-party apps require certain tables (usually related to content types)
    to have already been created.
    """
    def setup(self):
        self.INSTALLED_APPS = [app for app in self.INSTALLED_APPS
                              if app.startswith('django.') or app == 'south']


class Development(Debug):
    """
    Settings to simplify development. TODO: Split into 'local' and 'online'?
    TODO: Document how individual developers should subclass this and each use
    their own, in their own development environments.
    """
    _DEBUG_TOOLBAR_ENABLED = True
    _LOCAL_SOURCES = True


class Production(Base):
    pass


class Staging(Production):
    pass


# Instantitate a class specified by the DJANGO_SETTINGS_CLASS environment
# variable, and copy its (uppercase) attributes to this module's globals.
#
# Typically you want to tell virtualenvs to set the settings class to
# 'Development' or 'Production', as appropriate... or if this is a feature
# branch, create a sub-class of Development (assuming the feature, or its
# development, require strange new (or just different-from-default) settings).
cinch_django_settings(globals())
