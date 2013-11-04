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


def context_processor(request):
    """
    Project-level context processor; add template context variables relating
    to the entire project, or required by all templates.
    
    Currently this function just adds settings listed in
    ``_CONTEXT_SETTINGS_VARIABLES`` to the context.
    """
    # Inject settings listed in _CONTEXT_SETTINGS_VARIABLES into templates
    project_context = {setting_name: getattr(settings, setting_name)
                       for setting_name in settings._CONTEXT_SETTINGS_VARIABLES}
    return project_context
