
from django.conf.urls import patterns, url
#from ..views import debug as debug_views


urlpatterns = patterns(
    'hipikat.views.debug',
    url(r"^scratch/$", 'scratch', name="debug-scratch"),
    url(r"^blog-layout/$", 'blog_layout', name="blog_layout"),
)
