
from elephantblog import views as elephantblog_views


class BlogIndexView(elephantblog_views.ArchiveIndexView):
    paginate_by = None
    def get_queryset(self):
        qs = super(BlogIndexView, self).get_queryset()
        qs = qs.filter(is_featured=True)
        return qs
index = BlogIndexView.as_view()


class EntryDetailView(elephantblog_views.DateDetailView):

    def get_queryset(self):
        return elephantblog_views.ElephantblogMixin.get_queryset(self)
        #return super(EntryDetailView, self).get_queryset()

entry_detail = EntryDetailView.as_view()
