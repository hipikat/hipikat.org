
from django.conf import settings
from django.views.generic import TemplateView
from .common import NotConfiguredView       #, get_activity_items


class FrontPageView(TemplateView):
    template_name = 'front_page.html'

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)
        #context['activities'] = get_activity_items()
        return context

    def render_to_response(self, *args, **kwargs):
        response = super(FrontPageView, self).render_to_response(*args, **kwargs)
        #import pdb; pdb.set_trace()
        return response
front_page = FrontPageView.as_view()


# TODO
about = NotConfiguredView.as_view()
