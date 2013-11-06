"""
Configuration for django-hosts. Sets urlconf on the request to a module
under hipikat.urls matching the requested CNAME, if it's one of 'www' or
'blog'. (Outside of testing and development, it should be; configure the
web server should to redirect requests on hipikat.org/foo/bar
to www.hipikat.org/foo/bar)
"""

from django_hosts import patterns, host

host_patterns = patterns(
    'hipikat.urls',
    host(r'www', 'www', name='main_site'),
    host(r'blog', 'blog', name='blog'),
)
