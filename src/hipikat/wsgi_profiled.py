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
import envdir

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "hipikat.settings"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hipikat.settings.default")

BASE_DIR = dirname(dirname(dirname(__file__)))

# TODO: abstraction from where? uwsgi calls the virtualenv's local env
# stuff but but... not postactivate... so project_settings not in path?
envdir.read(join(BASE_DIR, 'var', 'env'))

from werkzeug.contrib.profiler import ProfilerMiddleware

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application


#application = get_wsgi_application()
profile_dir = join(BASE_DIR, 'var', 'profiler')

application = ProfilerMiddleware(get_wsgi_application(),
                                 profile_dir=profile_dir)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
