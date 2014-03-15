"""
While ROOT_URLCONF is set to 'hipikat.urls', this top level of the package
should never wind up as the urlconf in use; django-hosts will route to one
of the sub-modules, based on the requested domain.
"""

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django_hosts.reverse import reverse_full
try:
    from django.utils import timezone
    now = timezone.now
except ImportError:
    timezone = None
    from datetime import datetime
    now = datetime.now


# If this gets hit, it means django-hosts isn't working as expected
urlpatterns = patterns('hipikat.views.common', url(r'.*', 'NotConfiguredView'))


# Django admin interface and admin docs

# TODO: This fixes import order issues; fix with app-loading when we get Django 1.7
#from hipikat.models import fein

admin.autodiscover()

#from hipikat.models import Writing, WritingAdmin
#admin.site.register(Writing, WritingAdmin)

admin_urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
global_urlpatterns = admin_urlpatterns

# Enable views to aid debugging and development
if settings._DEBUG_URLPATTERNS_ENABLED:
    from . import _debug as debug_urls    # <.<
    debug_urlpatterns = patterns('', url(r'^:D/', include(debug_urls)))
    global_urlpatterns += debug_urlpatterns


### URL resolution overrides
def get_elephantblog_url(entry):
    # We use naive date using UTC for conversion for permalink
    if getattr(settings, 'USE_TZ', False):
        pub_date = timezone.make_naive(entry.published_on, timezone.utc)
    else:
        pub_date = entry.published_on
    return reverse_full(
        host='blog' if entry.entry_type == 'blog' else 'main_site',
        view='blog_entry_detail',
        view_kwargs={
            'year': pub_date.strftime('%Y'),
            'month': pub_date.strftime('%m'),
            'day': pub_date.strftime('%d'),
            'slug': entry.slug,
        }
    )
