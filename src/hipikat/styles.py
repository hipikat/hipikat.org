# coding=utf-8

def context_processor(request):
    style_context = {

        # This is going back in base.html since it makes more sense for hard-
        # coded style variables to live in templates than Python code...
        #
        # But I'm keeping this context processor here because I'm planning to
        # do something to switch between CDN-based and locally-stored copies of
        # libraries dynamically. (Both for development in cafés with no wi-fi
        # and … as an emergency switch if the site's design fails because of a
        # third-party/CDN network going down/playing up.
        #
        #'css_site_hrefs': [
        #    'http://fonts.googleapis.com/css?family=Roboto+Condensed:400,700|'
        #    'Roboto:400,400italic,500,700,700italic,300|Roboto+Slab:400,700',
        #],
    }
    return style_context
