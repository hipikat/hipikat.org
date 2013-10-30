# coding=utf-8

from django.conf.urls import patterns, url
from hipikat.views.debug import DebugTemplateListView

# Simple debugging utility URLs
urlpatterns = patterns(
    'hipikat.views.debug',
    # A safe way to get a page with not much on it to render; useful when you've
    # broken your base template and you just need some debug-toolbar output.
    url(r"^blank/$", 'blank', name="blank"),
)

# Template debugging - TODO: Move to a setting
exclude_template_patterns = [
    r'\.swp$',
    r'[-_\.]old',
]
urlpatterns += patterns(
    'hipikat.views.debug',
    # List templates under [templates/]debug/, and render them naïvely
    url(r"^templates/$",
        DebugTemplateListView.as_view(exclude_patterns=exclude_template_patterns),
        name="debug_template_list"),
    url(r"^templates/(?P<template_name>.+)$", 'debug_template_detail',
        name="debug_template_detail"),
)
