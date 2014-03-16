
#from elephantblog import views as elephantblog_views
#from elephantblog.models import Entry
from django.views.generic import TemplateView


class BlogIndexView(TemplateView):
    """Actually an index. Make this not-the-front-page later."""
    #paginate_by = None

    #def get_context_data(self, **kwargs):
    #    context = super(BlogIndexView, self).get_context_data(**kwargs)
    #    context['archive_title'] = r'Recent entries'
    #    return context

    #def get_queryset(self):
    #    qs = super(BlogIndexView, self).get_queryset()
    #    qs = qs.filter(is_active=True, is_final=True, entry_type='blog')
    #    return qs

index = BlogIndexView.as_view()
