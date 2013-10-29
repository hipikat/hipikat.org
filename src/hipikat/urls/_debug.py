# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'hipikat.views.debug',

    # A safe way to get a page with not much on it to render; useful when you've
    # broken your base template and you just need some debug-toolbar output.
    url(r"^debug/blank/$", 'blank', name="blank"),

    # List templates under [templates/]debug/, and render them naïvely
    #url(r"^debug/templates/$", 'debug_template_list', name="debug_template_list"),
    url(r"^debug/templates/(?P<template_name>.+)$",
        'debug_template_detail', name="debug_template_detail"),
)
