
from django.conf.urls import patterns, include, url
from ._global import urlpatterns
from ..views import www_landing_view


urlpatterns += patterns(
    '',

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),

    # Front page
    #url(r'^$', www_landing_view(), name="front_page"),

    url(r'', include('fluent_pages.urls')),
)
