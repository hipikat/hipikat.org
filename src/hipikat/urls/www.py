
from django.conf.urls import patterns, include, url


from . import global_urlpatterns


urlpatterns = global_urlpatterns + patterns(
    'hipikat.views',

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),

    # Front page
    url(r'^$', 'front_page', name="front_page"),

    #url(r'', include('fluent_pages.urls')),
)
