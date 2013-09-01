
from django.conf.urls import patterns, include, urls
from ._global import urlpatterns
from ..views import www_landing


urlpatterns += patterns(
    '',

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),

    # Front page
    url(r'^$', www_landing(), name="front_page"),
)
