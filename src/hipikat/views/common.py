
from django.views.generic import TemplateView


class NotConfiguredView(TemplateView):
    template_name = '404.html'
not_configured_view = NotConfiguredView.as_view()
