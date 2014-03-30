# coding=utf-8
"""
Settings for the Django project on http://hipikat.org/.
"""

#from functools import partial
from glob import glob
from itertools import chain
import os
from os import getenv, path
from os.path import dirname
import sys

from cinch import cinch_django_settings, CinchSettings
from dj_database_url import config as db_config
import envdir
#from cinch.mixins import FHSDirsMixin
#from .logging import FileLoggingMixin


class LocalSiteSettings(object):
    """Settings specific to this site."""


class DjangoCMSSettings(object):
    """Settings for Django CMS 3.0c1"""
    CMS_TEMPLATES = (
        ('template_1.html', 'Template One'),
    )
    LANGUAGES = [
        ('en', 'English'),
    ]
    CKEDITOR_SETTINGS = {
        'language': 'en',
        'toolbar': 'CMS',
        'skin': 'moono',
    }


class Base(
        LocalSiteSettings,
        DjangoCMSSettings,
        CinchSettings):

    # Main project module name
    PROJECT_MODULE_NAME = 'hipikat'
    # Repository root (assuming we are `{repo}/src/{project}/settings.py`)
    PROJECT_PATH = path.dirname(path.dirname(path.dirname(__file__)))
    # Repository checkout name
    DEPLOY_NAME = path.basename(PROJECT_PATH)

    # Load environment variables that aren't already set from var/env/*
    envdir.read(path.join(PROJECT_PATH, 'var', 'env'), no_clobber=True)

    # Site metadata
    ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
    MANAGERS = ADMINS
    LANGUAGE_CODE = 'en'
    SHORT_DATE_FORMAT = 'Y-m-d'
    SITE_ID = 1
    TIME_ZONE = 'Australia/West'

    # Runtime, debug & security settings…
    DEBUG = False
    TEMPLATE_DEBUG = False

    INTERNAL_IPS = tuple(set(eval(getenv('DJANGO_INTERNAL_IPS', '()')) + ('127.0.0.1',)))
    SECRET_KEY = getenv('DJANGO_SECRET_KEY')
    TESTING = True if 'test' in sys.argv else False
    WSGI_APPLICATION = PROJECT_MODULE_NAME + '.wsgi.application'

    # Directories, URLs
    ROOT_FQDN = getenv('DJANGO_ROOT_FQDN', 'hipikat.org')
    ALLOWED_HOSTS = ['.' + ROOT_FQDN]
    ROOT_URLCONF = PROJECT_MODULE_NAME + '.urls'
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    STATIC_ROOT = path.join(PROJECT_PATH, 'var', 'static')
    MEDIA_ROOT = path.join(PROJECT_PATH, 'var', 'media')
    TEMPLATE_DIRS = [path.join(PROJECT_PATH, 'src', 'templates')]
    FIXTURES_DIRS = [path.join(PROJECT_PATH, 'var', 'fixtures')]

    # Databases…
    DATABASES = dict(default=db_config(env='DJANGO_DATABASE_URL'))

    ### Request pipeline
    MIDDLEWARE_CLASSES = (
        #PROJECT_MODULE_NAME + '.style.ResourceRegistryMiddleware',
        #'django_hosts.middleware.HostsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        #PROJECT_MODULE_NAME + '.style.CleanHTMLMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
    )
    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        'cms.context_processors.cms_settings',
        'sekizai.context_processors.sekizai',
        PROJECT_MODULE_NAME + '.project_context_processor',
    ]

    # django-hosts
    #PARENT_HOST = ALLOWED_HOSTS[0] if ALLOWED_HOSTS[0][0] != '.' else ALLOWED_HOSTS[0][1:]
    #ROOT_HOSTCONF = PROJECT_MODULE_NAME + '.hosts'
    #DEFAULT_HOST = 'main_site'

    # Local file-system logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "\n%(levelname)s [%(asctime)s][%(pathname)s:%(lineno)s]" +
                          "[p/t:%(process)d/%(thread)d]\n%(message)s"
            },  
            'simple': {
                'format': '%(levelname)s [%(module)s:%(lineno)s] %(message)s'
            },  
        },  
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },  
        },  
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },  
        },  
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },  
        },  
    }

    def setup(self):
        """Configure settings which require initialised base classes/mixins."""
        super(Base, self).setup()

        # Settings which are `True` by default when `DEBUG` is `True`
        for debug_true_default in (
            'DEBUG_MIDDLEWARE_ENABLED',    # [project].middleware.Debug[Inner|Outer]Middleware
            'DEBUG_TOOLBAR_ENABLED',       # django-debug-toolbar
            'DEBUG_URLPATTERNS_ENABLED',   # Include [project].urls.debug_urlpatterns
            'LOCAL_RESOURCES'):             # Prevent linking to external resources
            self.setdefault(debug_true_default, self.DEBUG)

        # Settings which are `False` by default when `DEBUG` is `True`
        for debug_false_default in (
            'MINIFY_RESOURCES'):            # Request minified JavaScript/CSS resources
            self.setdefault(debug_false_default, not self.DEBUG)

        ### Static files
        self.STATICFILES_DIRS = [path.join(self.PROJECT_PATH, 'src', 'static')]
        for vend in glob(path.join(self.PROJECT_PATH, 'src', 'vendor', '*')):
            self.STATICFILES_DIRS.append((path.basename(vend), vend))
    #
    # end Baes.setup()

    ### Application setup
    INSTALLED_APPS = [
        ### Local apps
        PROJECT_MODULE_NAME,        # Current project

        ### Third-party apps
        'aldryn_blog',              # Aldryn Blog: https://github.com/aldryn/aldryn-blog
        'aldryn_common',
        'django_select2',
        'easy_thumbnails',
        'filer',
        'taggit',

        'djangocms_text_ckeditor',  # WSGI text editor for Django CMS (must be above 'cms')

        'cms',                      # Django CMS 3
        'mptt',                     # Modified pre-order traversal trees (for use by menus)
        'menus',                    # Helper for model-independent hierarchical website navigation
        'sekizai',                  # Used by Django CMS for JavaScript and CSS management
        'djangocms_admin_style',    # Django CMS admin skin


        #'cms.plugins.file',    # (must define a template first)
        #'cms.plugins.flash',    # (must define a template first)
        #'cms.plugins.googlemap',
        #'cms.plugins.picture',
        #'cms.plugins.teaser',
        #'djangocms_link',
        #'djangocms_snippet',
        #'cms.plugins.video',

        #'reversion',

        'south',                    # Database-agnostic migrations for Django applications
        'django_extensions',        # django-extensions: shell_plus, runserver_plus, etc.

        ### Django contrib apps
        'django.contrib.admin', 'django.contrib.admindocs', 'django.contrib.auth',
        'django.contrib.contenttypes', 'django.contrib.humanize', 'django.contrib.messages',
        'django.contrib.sessions', 'django.contrib.staticfiles', 'django.contrib.sites',
    ]


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
    #TEMPLATE_STRING_IF_INVALID = 'INVALID_CONTEXT<%s>'

    DEBUG_MIDDLEWARE_ENABLED = True
    DEBUG_TOOLBAR_ENABLED = True
    DEBUG_URLPATTERNS_ENABLED = True
    MINIFY_RESOURCES = False

    def setup(self):
        super(Debug, self).setup()

        # If tests are being run (added by NormaliseSettings)
        if self.TESTING and False:
            # Use an sqlite database while testing to violently increase test speed
            self.DATABASES['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': path.join(self.DB_DIR, 'test-run.db'),
            }

        # Enable django-debug-toolbar (as early as possible and no earlier)
        if self.DEBUG_TOOLBAR_ENABLED:
            insert_at = 0
            for pre_djtb in (
                'django.middleware.GZipMiddleware',
                'django_hosts.middleware.HostsMiddleware'):
                try:
                    insert_at = max(insert_at, (self.MIDDLEWARE_CLASSES.index(pre_djtb) + 1))
                except ValueError:
                    pass
            self.MIDDLEWARE_CLASSES = tuple(chain(
                self.MIDDLEWARE_CLASSES[0:insert_at],
                ('debug_toolbar.middleware.DebugToolbarMiddleware',),
                self.MIDDLEWARE_CLASSES[insert_at:]))
            self.INSTALLED_APPS.append('debug_toolbar')
            DEBUG_TOOLBAR_PATCH_SETTINGS = False

        # Request pipeline
        if self.DEBUG_MIDDLEWARE_ENABLED:
            self.MIDDLEWARE_CLASSES = tuple(chain([
                self.PROJECT_MODULE_NAME + '.middleware.DebugOuterMiddleware',
            ], self.MIDDLEWARE_CLASSES, [
                self.PROJECT_MODULE_NAME + '.middleware.DebugInnerMiddleware',
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
    LOCAL_RESOURCES = True
    DEBUG_TOOLBAR_ENABLED = False

    def setup(self):
        super(Development, self).setup()
        #self.ALLOWED_HOSTS = ['evilspa.dyndns.org'] + list(self.ALLOWED_HOSTS)
        #self.WSGI_APPLICATION = self.PROJECT_MODULE_NAME + '.wsgi.profiled_application'
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
