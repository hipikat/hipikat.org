# hipikat/__init__.py

from django.conf import settings


def context_processor(request):
    # Context variables pulled from django.conf.settings
    project_context = {setting_name: getattr(settings, setting_name)
                       for setting_name in settings._CONTEXT_SETTINGS_VARIABLES}

    return project_context
