
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'hipikat.views.debug',
    url(r"^scratch/$", 'scratch', name="debug-scratch"),
    url(r"^blog-layout/$", 'blog_layout', name="blog_layout"),
)
