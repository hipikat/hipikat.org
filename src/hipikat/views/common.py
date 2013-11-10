
from django.views.generic import TemplateView


class NotConfiguredView(TemplateView):
    template_name = 'layouts/page/error.html'
not_configured_view = NotConfiguredView.as_view()
