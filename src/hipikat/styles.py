
def context_processor(request):
    context = {
        'site_css_hrefs': 'http://fonts.googleapis.com/css?family=Roboto+Condensed:400,700|'
        'Roboto:400,400italic,500,700,700italic,300|Roboto+Slab:400,700',
    }
    return context
