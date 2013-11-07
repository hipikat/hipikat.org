# coding=utf-8
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage


RESOURCE_REGISTRY_NAME = settings.PROJECT_MODULE + '_resource_registry'


javascript_sources = {
    'zepto': '//cdnjs.cloudflare.com/ajax/libs/zepto/1.0/zepto.min.js',
    'tinymce': '//cdnjs.cloudflare.com/ajax/libs/tinymce/3.5.8/tiny_mce.js',
    'foundation': '//cdnjs.cloudflare.com/ajax/libs/foundation/4.3.2/js/foundation.min.js',
}
if settings._LOCAL_SOURCES:
    static_url = staticfiles_storage.url
    javascript_sources.update({
       'zepto': static_url('zepto/' + 'zepto.min.js' if settings.DEBUG else 'zepto.js'),
       'tinymce': static_url('tinymce/tinymce.min.js'),
       'foundation': static_url('zurb/foundation/foundation.js'),
    })

style_sources = {
    'roboto': 'http://fonts.googleapis.com/css?family=Roboto+Condensed'
    ':400,700|Roboto:400,400italic,500,700,700italic,300|Roboto+Slab:400,700',
}
if settings._LOCAL_SOURCES:
    style_sources.update({
        'roboto': static_url('fonts/roboto.css'),
    })


class ResourceRegistryMiddleware(object):
    """
    Attach a ResourceRegistry object to the request, since the required
    resources are specific to a request...
    """
    def process_request(self, request):
        setattr(request, RESOURCE_REGISTRY_NAME, ResourceRegistry())


class JavaScriptRequirements(object):
    """
    This is still mostly a stub for future plans, but it seems like a cleanish
    approach to switching between locally hosted and CDN-delivered static files.

    TODO: code anywhere before the template queries for javascripts should be
    able to register its requirement with hipikat.style.require_javascript('foo')

    TODO: Programmatically drop Zepto when jQuery is required?
    """
    def body(self):
        sources = (JavaScriptResource(script[1])
                   for script in javascript_sources.items()
                   if script[0] in ('zepto', 'foundation'))
        return sources


class JavaScriptResource(object):
    linked = True       # TODO: handle inline scripts
    def __init__(self, src, *args, **kwargs):
        self.src = src


class StyleResource(object):
    def __init__(self, href, *args, **kwargs):
        self.href = href


class ResourceRegistry(object):
    javascripts = JavaScriptRequirements()
    styles = [StyleResource(style[1]) for style in style_sources.items()]


def resources(request):
    return getattr(request, RESOURCE_REGISTRY_NAME)


#class CleanHTMLMiddleware(object):
#    def process_response(self, request, response):
#        content = response.content.split()
#        response.content =     # This is probably a stupid idea
