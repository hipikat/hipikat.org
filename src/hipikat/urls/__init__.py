# hipikat/urls/__init__.py

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from hipikat.views import front_page


admin.autodiscover()


urlpatterns = patterns(
    '',
    # Django admin and admin docs
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Blog
    #url(r'^blog/', include('fluent_blogs.urls')),

    # Fluent pages
    #url(r'', include('fluent_pages.urls')),

    # Front page
    url(r'^$', front_page(), name="front_page"),
)
