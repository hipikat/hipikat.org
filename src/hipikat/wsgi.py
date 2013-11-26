"""
WSGI config for hipikat project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
from os.path import join, dirname
from django.conf import settings
from django.core.wsgi import get_wsgi_application
import envdir


# Main application used by WSGI servers pointed at the hipikat.wsgi module
application = get_wsgi_application()

# Werkzeug profiler - http://werkzeug.pocoo.org/docs/contrib/profiler/
if getattr(settings, 'WSGI_PROFILER_ENABLED', False):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    application = ProfilerMiddleware(application,
                                     profile_dir=join(settings.VAR_DIR, 'profiler'))

