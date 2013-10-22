
from django.conf.urls import patterns, include, url


from . import global_urlpatterns


urlpatterns = global_urlpatterns + patterns(
    '',
    url(r'^admin/util/taggit_autocomplete_modified/',
        include('taggit_autocomplete_modified.urls')),
    url(r'^', include('fluent_blogs.urls')),
)
