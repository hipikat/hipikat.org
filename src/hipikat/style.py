# coding=utf-8
from django.conf import settings


STATIC_URL = settings.STATIC_URL
RESOURCE_REGISTRY_NAME = settings.PROJECT_MODULE + '_resource_registry'


def _min_str(minify=None):
    if minify is not None:
        return '.min' if minify else ''
    else:
        return '.min' if settings._MINIFY_RESOURCES else ''


def javascripts(minify=None, local=False):
    """
    Return a dict of keys (short names) for JavaScript libraries and their
    URLs. CDN-delivered sources are returned, rather than local copies,
    if ``local`` is ``False``. Minified versions are returned (if possible)
    if ``minify`` is ``True``. TODO: Version switching? django-pipeline instead?
    """
    dotmin = _min_str(minify)
    CDNJS_LIBS = '//cdnjs.cloudflare.com/ajax/libs/'
    cdn_sources = {
        'foundation': '{}foundation/4.3.2/js/foundation.min.js'.format(CDNJS_LIBS),
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery{}.js'.format(dotmin),
        'tinymce': '{}tinymce/3.5.8/tiny_mce.js'.format(CDNJS_LIBS),
        'zepto': '{}zepto/1.0/zepto{}.js'.format(CDNJS_LIBS, dotmin),
    }
    local_sources = {
        'foundation': STATIC_URL + 'zurb/foundation/foundation.js',
        'jquery': STATIC_URL + 'jquery/jquery-1.10.2{}.js'.format(dotmin),
        'tinymce': STATIC_URL + 'tinymce/tinymce.min.js',        # TODO: Find un-minified version
        'zepto': STATIC_URL + 'zepto/zepto{}.js'.format(dotmin),
    }
    # Make sure we include every listed library, even if a local/remote
    # source isn't available as requested
    sources, alt_sources = (local_sources, cdn_sources) if local else (cdn_sources, local_sources)
    for missing in set(alt_sources) - set(sources):
        sources[missing] = alt_sources[missing]
    return sources


def stylesheets(minify=None, local=False):
    """
    Return a dict of keys (short names) for stylesheets and their URLs.
    CDN-delivered sources are returned, rather than local copies,
    if ``local`` is ``False``. Minified versions are returned (if possible)
    if ``minify`` is ``True``. TODO: Version switching? django-pipeline instead?
    """
    dotmin = _min_str(minify)
    cdn_sources = {
        'font-awesome': '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css',
        #'roboto': 'http://fonts.googleapis.com/css?family=Roboto+Condensed'
        #':400,700|Roboto:400,400italic,500,700,700italic,300|Roboto+Slab:400,700',
        #'cloud-typography': 'http://cloud.typography.com/7646652/805902/css/fonts.css',
        'cloud-typography': '//cloud.typography.com/7646652/805902/css/fonts.css',
    }
    local_sources = {
        'pygment-styles': STATIC_URL + 'stylesheets/pygment-styles.css',
        'font-awesome': STATIC_URL + 'font-awesome/css/font-awesome{}.css'.format(dotmin),
        #'roboto': STATIC_URL + 'fonts/roboto.css',
    }
    # Make sure we include every listed library, even if a local/remote
    # source isn't available as requested
    sources, alt_sources = (local_sources, cdn_sources) if local else (cdn_sources, local_sources)
    for missing in set(alt_sources) - set(sources):
        sources[missing] = alt_sources[missing]
    return sources


### The resource registry is basically an object attached to the request TODOLipsum
class JavaScriptRequirements(object):
    """
    This is still mostly a stub for future plans, but it seems like a cleanish
    approach to switching between locally hosted and CDN-delivered static files.
    An object of this class gets attached to the 'resources' object templates
    see as 'javascript', so {{ resources.javascripts.body }} is a list of
    ``JavaScriptResource`` objects.
    TODO: code anywhere before the template queries for javascripts should be
    able to register its requirement with hipikat.style.require_javascript('foo')
    TODO: Programmatically drop Zepto when jQuery is required? (and so on?)
    """
    def head(self):
        """
        Return a list of JavaScript sources to be included in the page <head>.
        """
        return []   # AS IT SHOULD BE! (Apparently.)

    def body(self):
        """
        Return a list of JavaScript sources to be included before the closing
        </body> tag of a page.
        TODO: Base sets of required resources should be template-defined…
        """
        sources = [JavaScriptResource(script[1])
                   for script in javascripts().items()
                   if script[0] in ('zepto', 'foundation')]
        return sources


class JavaScriptResource(object):
    """
    Representation of a JavaScript file or chunk of code. Must have a
    ``src`` attribute if ``linked is True``, or ``code`` if it is
    ``False``. ``linked is not inline``. TODO: Most of it.
    """
    linked = True       # TODO: handle inline scripts

    def __init__(self, src, *args, **kwargs):
        self.src = src

    def inline(self):
        return not self.linked


class StyleResource(object):
    """
    Representation of a stylesheet file or definition. Must have a
    ``href`` attribute if ``linked is True``, or ``code`` if it is
    ``False``. ``linked is not inline``. TODO: Most of it.
    """
    linked = True

    def __init__(self, href, *args, **kwargs):
        self.href = href

    def inline(self):
        return not self.linked


class ResourceRegistry(object):
    """
    A registry of resources required by a page, typically intended to be
    accessed by a template. Contains two lists of resource objects with
    the names ``javascripts`` and ``styles``.
    """
    def __init__(self, *args, **kwargs):
        self.javascripts = JavaScriptRequirements()
        self.stylesheets = [StyleResource(style[1]) for style in stylesheets().items()]


def resources(request):
    """
    Return the resource registry attached to a request, or create and
    attach a new one, and return that, if none exists.
    """
    if not hasattr(request, RESOURCE_REGISTRY_NAME):
        setattr(request, RESOURCE_REGISTRY_NAME, ResourceRegistry())
    return getattr(request, RESOURCE_REGISTRY_NAME)


# TODO: Deprecate? resources(request) does just as much...
#class ResourceRegistryMiddleware(object):
#    """
#    Attach a ResourceRegistry object to the request, since the required
#    resources are specific to a request...
#    """
#    def process_request(self, request):
#        setattr(request, RESOURCE_REGISTRY_NAME, ResourceRegistry())


# TODO: Either make your HTML really pretty, or abandon this completely.
# The advantage could be auto-detection of invalid markup... Mmmm...
#class CleanHTMLMiddleware(object):
#    def process_response(self, request, response):
#        content = response.content.split()
#        response.content =     # This is probably a stupid idea
