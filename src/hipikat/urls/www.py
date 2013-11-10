
from django.conf.urls import patterns, include, url


from . import global_urlpatterns


urlpatterns = global_urlpatterns

urlpatterns += patterns('',
    url(r'^scraps/', include('elephantblog.urls')),
)

urlpatterns += global_urlpatterns + patterns(
    'hipikat.views',

    # Front page
    url(r'^$', 'front_page', name="front_page"),

    # Let feinCMS do the work, so humans have time to relax
    url(r'', include('feincms.urls')),

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),


    #url(r'', include('fluent_pages.urls')),
)
