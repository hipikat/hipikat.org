
from django.shortcuts import render
from django.views.generic import TemplateView


def blank(request):
    return render(request, "layouts/blank.html")


class DebugTemplateDetailView(TemplateView):
    """
    Render a template in 'debug/<template_name>.html'.
    """
    def get(self, request, *args, **kwargs):
        self.template_name = kwargs['template_name']
        return super(DebugTemplateDetailView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        return ['debug/{}.html'.format(self.template_name)]

debug_template_detail = DebugTemplateDetailView.as_view()


class DebugTemplateListView(TemplateView):
    """
    List HTML files under each directory in ``settings.TEMPLATE_DIRS``,
    with links to the named URL ``debug_template_detail``, using the
    filename (sans '.html' extension) as the ``template_name`` keyword.
    TODO: Implement, once you've got a basic template to put it in :P
    """
    def get_context_data(self, **kwargs):
        kwargs['templates'] = TemplateFiles()
        return super(DebugTemplateListView, self).get_context_data(kwargs)

debug_template_list = DebugTemplateListView.as_view()
