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

# Django admin interface and admin docs
admin_urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Sub-modules should extend their urlpatterns with global_urlpatterns
# global_urlpatterns currently comprises:
# - Django admin and admin docs
# - Debug urlpatterns (if DEBUG is True)
global_urlpatterns = admin_urlpatterns
if settings.DEBUG_URLPATTERNS_ENABLED:
    from ._debug import urlpatterns as debug_patterns
    global_urlpatterns += debug_patterns

