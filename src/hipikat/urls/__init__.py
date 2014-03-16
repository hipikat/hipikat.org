"""
While ROOT_URLCONF is set to 'hipikat.urls', this top level of the package
should never wind up as the urlconf in use; django-hosts will route to one
of the sub-modules, based on the requested domain.
"""

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django_hosts.reverse import reverse_full
try:
    from django.utils import timezone
    now = timezone.now
except ImportError:
    timezone = None
    from datetime import datetime
    now = datetime.now


# If this gets hit, it means django-hosts isn't working as expected
urlpatterns = patterns('hipikat.views.common', url(r'.*', 'NotConfiguredView'))


# Django admin interface and admin docs
admin.autodiscover()
global_urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Enable views to aid debugging and development
if settings.DEBUG:
    import debug_toolbar
    global_urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

if settings._DEBUG_URLPATTERNS_ENABLED:
    from . import _debug as debug_urls    # <.<
    debug_urlpatterns = patterns('', url(r'^:D/', include(debug_urls)))
    global_urlpatterns += debug_urlpatterns
