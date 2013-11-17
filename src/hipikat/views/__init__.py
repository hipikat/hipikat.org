
from django.conf import settings
from django.views.generic import TemplateView
from .common import NotConfiguredView, get_activity_items


__all__ = ['FrontPageView', 'main_landing_view',]


class FrontPageView(TemplateView):
    template_name = 'front_page.html'

    def get_context_data(self, **kwargs):
        context['activity'] = get_activity_items(settings._MAX_RECENT_ACTIVITY_ITEMS)

    def render_to_response(self, *args, **kwargs):
        response = super(FrontPageView, self).render_to_response(*args, **kwargs)
        #import pdb; pdb.set_trace()
        return response

front_page = FrontPageView.as_view()


about = NotConfiguredView.as_view()
