
from django.conf.urls import patterns, include, url
from django.contrib import admin


__all__ = ['urlpatterns']


admin.autodiscover()


urlpatterns = patterns(
    '',
    # Django admin and admin docs
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
