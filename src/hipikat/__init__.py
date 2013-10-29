# hipikat/__init__.py

from django.conf import settings


CONTEXT_SETTINGS_VARIABLES = (
    'PROJECT_MODULE',
)

def context_processor(request):
    #project_context = {}
    #for setting_name in CONTEXT_SETTINGS_VARIABLES:
    #    project_context[setting_name] = getattr(settings, setting_name)

    # Context variables pulled from django.conf.settings
    project_context = {setting_name: getattr(settings, setting_name)
                        for setting_name in CONTEXT_SETTINGS_VARIABLES }

    return project_context
