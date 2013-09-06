
from django.conf.urls import patterns, include, url
from ..views import main_landing_view


from ._global import urlpatterns


urlpatterns += patterns(
    '',

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),

    # Front page
    url(r'^$', main_landing_view(), name="front_page"),

    url(r'', include('fluent_pages.urls')),
)
