"""URLconf for the main site; everything under http://www.hipikat.org/."""

from django.conf.urls import patterns, include, url
from . import global_urlpatterns


www_urlpatterns = patterns(
    'hipikat.views',
    url(r'^$', 'front_page', name="front_page"),
    url(r'^scraps/$', 'scraps.index', name="scraps_index"),
    url(r'^about/$', 'about', name="about"),
    #url(r'', include('feincms.urls')),
)
urlpatterns = global_urlpatterns + www_urlpatterns
