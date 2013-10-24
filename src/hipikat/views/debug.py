
from django.shortcuts import render


def scratch(request):
    return render(request, "debug/scratch.html")


def blog_layout(request):
    return render(request, "dev/blog-layout.html")


