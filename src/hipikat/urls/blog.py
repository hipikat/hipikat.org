
from django.conf.urls import patterns, include, url
from elephantblog.feeds import EntryFeed
#from elephantblog import views as elephantblog_views
from hipikat.views import blog as blog_views
from . import global_urlpatterns


"""
Blog URL patterns. These specialise the elephantblog setup by only
referencing 'featured' entires on the main blogroll.
"""
blog_patterns = patterns(
    'hipikat.views.blog',
    url(r'^feed/$', EntryFeed()),
    url(r'^$', 'index', name='blog_index'),
    #url(r'^(?P<year>\d{4})/$',
    #    views.YearArchiveView.as_view(**list_kwargs),
    #    name='elephantblog_entry_archive_year'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
    #    views.MonthArchiveView.as_view(**list_kwargs),
    #    name='elephantblog_entry_archive_month'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
    #    views.DayArchiveView.as_view(**list_kwargs),
    #    name='elephantblog_entry_archive_day'),
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
    #    views.DateDetailView.as_view(**detail_kwargs),
    #    name='elephantblog_entry_detail'),
    #url(r'^category/(?P<slug>[-\w]+)/$',
    #    views.CategoryArchiveIndexView.as_view(**list_kwargs),
    #    name='elephantblog_category_detail'),
)
urlpatterns = global_urlpatterns + blog_patterns
