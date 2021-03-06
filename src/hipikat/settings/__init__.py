# coding=utf-8
"""
Settings for the Django project on http://hipikat.org/.
"""

from itertools import chain
from os import getenv, path, environ
from os.path import dirname
import envdir
from cinch import cinch_django_settings, CinchSettings, NormaliseSettings
from cinch.mixins import FHSDirsMixin
#from project_settings import DIRS as PROJECT_DIRS
from .logging import FileLoggingMixin



def get_elephantblog_url(entry):
    """
    We can't import antyhing from the urls module before settings are loaded,
    and ABSOLUTE_URL_OVERRIDES doesn't take dotted-string arguments in place
    of callables, and this URL resolution function belongs in hipikat.urls,
    so this function is basically a lazy pass-through for blog URL resolution.
    """
    from hipikat.urls import get_elephantblog_url
    return get_elephantblog_url(entry)


class LocalSiteSettings(object):
    """Settings specific to this site."""
    _BLOG_INDEX_PREVIEWS = 10
    SITE_MAX_RECENT_ACTIVITY_ITEMS = 99


class Base(
        # Set {LIB,VAR,ETC,SRC,DB,LOG}_DIR settings, relative to BASE_DIR
        FHSDirsMixin,
        #PROJECT_DIRS,
        # Normalise settings to sensible defaults, add some conveniences
        NormaliseSettings,
        # Hard-coded (bad!) settings specific to hipikat.org
        LocalSiteSettings,
        # Basic file logging, to var/log/, with rotating 5M files (or thereabouts).
        FileLoggingMixin,
        # Base class for a django-cinch settings class
        CinchSettings):


    FEINCMS_USE_PAGE_ADMIN = False


    #       .../[repo]     /src         /hipikat     /settings    /__init__.py
    BASE_DIR = path.dirname(path.dirname(path.dirname(path.dirname(__file__))))
    DEPLOY_NAME = path.basename(BASE_DIR)
    PROJECT_MODULE = 'hipikat'

    # Read defaults from var/env/ - envdir writes environment variables for all
    # files regardless of whether the environ variable is set, so updating the
    # environment with a copy of the 'original' environment makes envdir's
    # behaviour effectively only set variables that haven't been set explicitly.
    # TODO: Write and submit a patch and tests for envdir.read_defaults().
    original_env = environ.copy()
    envdir.read(path.join(BASE_DIR, 'var', 'env'))
    environ.update(original_env)

    ### Project metadata
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    ROOT_FQDN = getenv('DJANGO_ROOT_FQDN', 'hipikat.org')
    ALLOWED_HOSTS = ['.' + ROOT_FQDN]
    LANGUAGE_CODE = 'en-au'
    TIME_ZONE = 'Australia/West'
    SHORT_DATE_FORMAT = 'Y-m-d'
    SECRET_KEY = getenv('DJANGO_SECRET_KEY')

    ### Private project settings
    # Settings variables injected into context
    _CONTEXT_SETTINGS_VARIABLES = [
        'PROJECT_MODULE',
        'SITE_MAX_RECENT_ACTIVITY_ITEMS',
    ]

    ### Debug
    DEBUG = False

    ### Databases…
    DATABASES = { 
        'default': {
            'USER': 'hipikat',
            'NAME': DEPLOY_NAME,
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '127.0.0.1',
            'PASSWORD': 'insecure',
        }   
    }

    ### Request pipeline
    MIDDLEWARE_CLASSES = [
        #PROJECT_MODULE + '.style.ResourceRegistryMiddleware',
        'django_hosts.middleware.HostsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.locale.LocaleMiddleware',
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
        'feincms.context_processors.add_page_if_missing',
        PROJECT_MODULE + '.project_context_processor',
    ]
    ROOT_URLCONF = PROJECT_MODULE + '.urls'

    # django-hosts
    PARENT_HOST = ALLOWED_HOSTS[0] if ALLOWED_HOSTS[0][0] != '.' else ALLOWED_HOSTS[0][1:]
    ROOT_HOSTCONF = PROJECT_MODULE + '.hosts'
    #DEFAULT_HOST = 'main_site'
    DEFAULT_HOST = 'not_configured'

    def setup(self):
        """Configure settings which require initialised base classes/mixins."""
        super(Base, self).setup()

        

        ### Debugging, testing, development
        # By default, set to True for debugging, False in production
        for debug_true_default in (
            '_DEBUG_MIDDLEWARE_ENABLED',    # [project].middleware.Debug[Inner|Outer]Middleware
            '_DEBUG_TOOLBAR_ENABLED',       # django-debug-toolbar
            '_DEBUG_URLPATTERNS_ENABLED',   # Include [project].urls.debug_urlpatterns
            '_LOCAL_RESOURCES',             # Prevent linking to external resources
        ):
            self.setdefault(debug_true_default, self.DEBUG)
        # By default, set to False while debugging, True in production
        for debug_false_default in (
            '_MINIFY_RESOURCES',            # Request minified JavaScript/CSS resources
        ):
            self.setdefault(debug_false_default, not self.DEBUG)

        ### Static files
        self.STATICFILES_DIRS = [
            path.join(self.SRC_DIR, 'static'),
            ('jquery', path.join(self.LIB_DIR, 'jquery-1.10.2')),
            ('tinymce', path.join(self.LIB_DIR, 'tinymce-4.0.10', 'js', 'tinymce')),
            ('zepto', path.join(self.LIB_DIR, 'zepto-1.0')),
            ('zurb', path.join(self.LIB_DIR, 'zurb-foundation', 'js')),
            ('font-awesome', path.join(self.LIB_DIR, 'Font-Awesome')),
        ]

        ### feinCMS
        self.FEINCMS_RICHTEXT_INIT_CONTEXT = {
            'TINYMCE_JS_URL': self.STATIC_URL + 'tinymce/tinymce.min.js',
        }
        self.FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce4.html'
    #
    # end def setup()

    ### Application setup
    INSTALLED_APPS = [
        ### Local apps
        PROJECT_MODULE,         # This project
        'revkom',               # revkom-helpers: Software patterns, utils, mixins etc
        ### Third-party apps
        'south',                # South: Database-agnostic migrations for Django applications
        'django_extensions',    # django-extensions: shell_plus, runserver_plus, etc.
        'django_hosts',         # django-hosts: Routes to urlconfs based on the requested domain
        'mptt',                 # django-mptt: Modified pre-order traversal trees
        'feincms', 'feincms.module.page', 'feincms.module.medialibrary',
        'elephantblog',
        ### Django contrib apps
        'django.contrib.admin', 'django.contrib.admindocs', 'django.contrib.auth',
        'django.contrib.contenttypes', 'django.contrib.humanize', 'django.contrib.messages',
        'django.contrib.sessions', 'django.contrib.staticfiles', 'django.contrib.sites',
    ]
    ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.entry': get_elephantblog_url,
        #'elephantblog.categorytranslation': elephantblog_categorytranslation_url,      # TODO
    }
    SOUTH_MIGRATION_MODULES = {
        'page': PROJECT_MODULE + '.migrate_apps.page',
        'elephantblog': PROJECT_MODULE + '.migrate_apps.elephantblog',
        'medialibrary': PROJECT_MODULE + '.migrate_apps.medialibrary',
    }


class Debug(Base):
    """
    Settings for debugging. This class attempts to remain close to a
    production profile, while switching on more debugging features and
    increasing logging output. For development, use Development.
    """
    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    TEMPLATE_STRING_IF_INVALID = 'INVALID_CONTEXT<%s>'

    _DEBUG_MIDDLEWARE_ENABLED = True
    _DEBUG_TOOLBAR_ENABLED = True
    _DEBUG_URLPATTERNS_ENABLED = True
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

        # Enable django-debug-toolbar
        if self._DEBUG_TOOLBAR_ENABLED:
            self.MIDDLEWARE_CLASSES = tuple(chain(
                list(self.MIDDLEWARE_CLASSES),
                ['debug_toolbar.middleware.DebugToolbarMiddleware']))
            self.INSTALLED_APPS = list(chain(
                self.INSTALLED_APPS,
                ['debug_toolbar']
            ))

        # Request pipeline
        if self._DEBUG_MIDDLEWARE_ENABLED:
            self.MIDDLEWARE_CLASSES = tuple(chain([
                self.PROJECT_MODULE + '.middleware.DebugOuterMiddleware',
            ], self.MIDDLEWARE_CLASSES, [
                self.PROJECT_MODULE + '.middleware.DebugInnerMiddleware',
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
    _LOCAL_RESOURCES = True

    def setup(self):
        super(Development, self).setup()
        #self.ALLOWED_HOSTS = ['evilspa.dyndns.org'] + list(self.ALLOWED_HOSTS)
        #self.WSGI_APPLICATION = self.PROJECT_MODULE + '.wsgi.profiled_application'
        #environ['TEST_FOO_BAR'] = str(True)


class Production(Base):
    pass


class ProductionProfiler(Production):
    """Enable the Werkzeug profile around a Production settings profile."""
    WSGI_PROFILER_ENABLED = True


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
