
from django_hosts import patterns, host

host_patterns = patterns(
    'hipikat.urls',
    host(r'www', 'www', name='main'),
    host(r'blog', 'blog', name='blog'),
)
