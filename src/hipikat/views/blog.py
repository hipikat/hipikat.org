
from elephantblog import views as elephantblog_views
from elephantblog.models import Entry


class BlogIndexView(elephantblog_views.ArchiveIndexView):
    paginate_by = None
    def get_context_data(self, **kwargs):
        context = super(BlogIndexView, self).get_context_data(**kwargs)
        context['archive_title'] = r'Recent entries'
        return context
    def get_queryset(self):
        qs = super(BlogIndexView, self).get_queryset()
        qs = qs.filter(is_active=True, is_final=True, entry_type='blog')
        return qs
index = BlogIndexView.as_view()


class EntryDetailView(elephantblog_views.DateDetailView):

    def get_queryset(self):
        """
        This gets around what I believe is a bug in elephantviews;
        DateDetailView never calls super, which is what prefetches categories.
        """
        #return elephantblog_views.ElephantblogMixin.get_queryset(self)
        return super(EntryDetailView, self).get_queryset()

entry_detail = EntryDetailView.as_view()
