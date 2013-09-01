
from django.http import HttpResponse

from django.conf.urls import patterns, include, url 
from django.contrib import admin
from ._global import urlpatterns


def foo_view(request):
    html = "<html><body>Hostess works.</body></html>"
    return HttpResponse(html)


urlpatterns += patterns(
    '',
    url('^$', foo_view),
)
