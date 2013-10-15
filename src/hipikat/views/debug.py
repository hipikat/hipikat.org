
from django.shortcuts import render


def blog_layout(request):
        return render(request, "dev/blog-layout.html")


