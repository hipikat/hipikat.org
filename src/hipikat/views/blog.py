
from elephantblog import views as elephantblog_views


class BlogIndexView(elephantblog_views.ArchiveIndexView):
    paginate_by = None
    def get_queryset(self):
        qs = super(BlogIndexView, self).get_queryset()
        qs = qs.filter(is_featured=True)
        return qs
index = BlogIndexView.as_view()


class EntryDetailView(elephantblog_views.DateDetailView):
    pass
entry_detail = EntryDetailView.as_view()
