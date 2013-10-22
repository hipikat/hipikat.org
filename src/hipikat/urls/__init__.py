"""
While ROOT_URLCONF is set to 'hipikat.urls', this top level of the package
should never wind up as the urlconf in use; django-hosts will route to one
of the sub-modules, based on the requested domain.
"""

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin


__all__ = ['urlpatterns']


# Should never be hit; see module docstring
urlpatterns = patterns(
    'hipikat.views.common',
    url('^', 'NotConfiguredView'),
)

# Sub-modules should extend their urlpatterns from this base
global_urlpatterns = patterns(
    '', 
    # Django admin and admin docs
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)


if settings.DEBUG_URLPATTERNS_ENABLED:
    from ._debug import urlpatterns as debug_patterns
    urlpatterns += debug_patterns

