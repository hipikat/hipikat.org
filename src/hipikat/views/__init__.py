
from django.views.generic import TemplateView


class FrontPageView(TemplateView):
    template_name = 'front-page.html'
front_page = FrontPageView.as_view
