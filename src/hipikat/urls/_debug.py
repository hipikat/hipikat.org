
from django.conf.urls import patterns, url




urlpatterns = patterns(
    'hipikat.views.debug',
    url(r"^scratch/$", 'scratch', name="debug-scratch"),
    url(r"^blank/$", 'blank', name="blank"),
    url(r"^blog-layout/$", 'blog_layout', name="blog_layout"),
    url(r"^templates/$", 'page_template_list', name="page_template_list"),
    url(r"^templates/(?P<template_name>.+)$", 'page_template_detail', name="list_page_templates"),
)
