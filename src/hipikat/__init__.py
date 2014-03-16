"""
The 'hipikat' package serves as the main app for the Django project
served at http://hipikat.org/. Besides containing settings, host and url
configuration, and offering the WSGI application entry-point, views and
models which aren't generic enough to be split into their own apps, or
which subclass third-party apps to add specialised behaviour, live here.

This file, the top-level module for the package, contains objects at the
the core of the of the site, likely to be used during the processing of
most requests.
"""
from django.conf import settings


def project_context_processor(request):
    """
    Project-level context processor; add template context variables relating
    to the entire project, or required by all templates.
    """
    # Inject some variables directly from settings
    context = {setting_name: getattr(settings, setting_name)
               for setting_name in getattr(settings, 'SETTINGS_AVAILABLE_TO_TEMPLATES', [])}

    # Accessor for JavaScript and stylesheet resources
    from .style import resources
    context['resources'] = resources(request)

    # Debug-time context
    if settings.DEBUG:
        # Rendering {{ raise_exception }} does just that. (Useful with runserver_plus.)
        from .utils import raise_exception
        context['raise_exception'] = raise_exception

    return context
