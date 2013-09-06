
from django.conf.urls import patterns, include, url
from django.shortcuts import render


def blog_layout(request):
    return render(request, "dev/blog-layout.html")


urlpatterns = patterns(
    "",
    url(r"^blog-layout/$", blog_layout, name="blog_layout"),
)
