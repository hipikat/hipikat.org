
from django.conf.urls import patterns, include, url
from . import global_urlpatterns



from django.conf.urls import patterns, include, url

from elephantblog.feeds import EntryFeed
from elephantblog import views


def elephantblog_patterns(list_kwargs={}, detail_kwargs={}):
    """
    Returns an instance of ready-to-use URL patterns for the blog.

    In the future, we will have a few configuration parameters here:

    - A parameter to specify a custom mixin for all view classes (or for
      list / detail view classes?)
    - Parameters to specify the language handling (probably some initialization
      arguments for the ``as_view`` methods)
    - The format of the month (three chars or two digits)
    - etc.
    """
    return patterns('',
        url(r'^feed/$', EntryFeed()),
        url(r'^$',
            views.ArchiveIndexView.as_view(**list_kwargs),
            name='elephantblog_entry_archive'),
        url(r'^(?P<year>\d{4})/$',
            views.YearArchiveView.as_view(**list_kwargs),
            name='elephantblog_entry_archive_year'),
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
            views.MonthArchiveView.as_view(**list_kwargs),
            name='elephantblog_entry_archive_month'),
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
            views.DayArchiveView.as_view(**list_kwargs),
            name='elephantblog_entry_archive_day'),
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
            views.DateDetailView.as_view(**detail_kwargs),
            name='elephantblog_entry_detail'),
        url(r'^category/(?P<slug>[-\w]+)/$',
            views.CategoryArchiveIndexView.as_view(**list_kwargs),
            name='elephantblog_category_detail'),
    )


# Backwards compatibility: Create a URL patterns object with the default
# configuration
urlpatterns = global_urlpatterns + elephantblog_patterns()

#urlpatterns += patterns('hipikat.views.common', url(r'foo', 'not_configured_view'))
