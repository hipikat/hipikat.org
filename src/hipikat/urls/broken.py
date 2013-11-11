"""URLconf for the main site; everything under http://www.hipikat.org/."""

from django.conf.urls import patterns, include, url
from . import global_urlpatterns


www_urlpatterns = patterns(
    'hipikat.views.common',
    url(r'^$', 'not_configured_view', name="broken_landing_page"),
)
urlpatterns = global_urlpatterns + www_urlpatterns
