
from django.shortcuts import render
from django.views.generic import TemplateView


def blank(request):
    return render(request, "layouts/blank.html")

class PageTemplateDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        #import pdb; pdb.set_trace()
        return super(TemplateView, self).get_template_names()
page_template_detail = PageTemplateDetailView.as_view()


class PageTemplateListView(TemplateView):
    def get_context_data(self, **kwargs):
        kwargs['templates'] = TemplateFiles()
        return super(PageTemplateListView, self).get_context_data(kwargs)
page_template_list = PageTemplateListView.as_view()


def blog_layout(request):
    return render(request, "dev/blog-layout.html")


def scratch(request):
    return render(request, "debug/scratch.html")


