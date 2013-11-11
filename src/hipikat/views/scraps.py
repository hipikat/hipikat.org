
from django.views.generic import TemplateView


class ScrapsIndexView(TemplateView):
    template_name = '404.html'
index = ScrapsIndexView.as_view()
