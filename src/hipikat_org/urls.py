"""
URL configuration for Hipikat.org

About: https://docs.djangoproject.com/en/1.8/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from hipikat_org.views import development as dev_views


urlpatterns = [
    # Django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        # Template development
        url(r'^_dev/templates/(?P<template_name>.+)$',
            dev_views.TemplateDetail.as_view(),
            name='template_detail',
            ),
        url(r'^_dev/templates/$',
            dev_views.TemplateList.as_view(),
            name='template_list',
            ),
        # Simple redirects
        url(r'^dev/$',
            RedirectView.as_view(pattern_name='template_list'),
            name='redirect_to_development'
            ),
    )
