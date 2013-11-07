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


class ResourceRegistryMiddleware(object):
    def process_request(self, request):
        setattr(request, RESOURCE_REGISTRY_NAME, ResourceRegistry())


class JavaScriptRequirements(object):
    """
    TODO: code anywhere before the template queries for javascripts should be
    able to register its requirement with hipikat.style.require_javascript('foo')
    """
    def body():
        #return {script[0]: script[1] for script in javascript_sources
        #        if script[0] in ('zepto', 'foundation')}
        sources = (JavaScriptResource(script[1]) for script in javascript_sources
                if script[0] in ('zepto', 'foundation'))
        from pprint import pprint
        pprint(sources)
        return sources


class ResourceRegistry(object):
    javascripts = JavaScriptRequirements()


class JavaScriptResource(object):
    linked = True

    def __init__(self, src, *args, **kwargs):
        self.src = src


def resources(request):
    return getattr(request, RESOURCE_REGISTRY_NAME)
