
from django.conf.urls import patterns, include, url


from ._global import urlpatterns


urlpatterns += patterns(
    '',
    url(r'^admin/util/taggit_autocomplete_modified/',
        include('taggit_autocomplete_modified.urls')),
    url(r'^', include('fluent_blogs.urls')),
)
