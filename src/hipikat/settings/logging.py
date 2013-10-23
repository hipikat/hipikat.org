"""
Define the base logging dictionary 
"""
from cinch import CinchSettings


class FileLoggingMixin(CinchSettings):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "\n%(levelname)s [%(asctime)s][%(pathname)s:%(lineno)s]" +
                          "[p/t:%(process)d/%(thread)d]\n%(message)s"
            },  
            'simple': {
                'format': '%(levelname)s [%(module)s:%(lineno)s] %(message)s'
            },  
        },  
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },  
        },  
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },  
        },  
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },  
        },  
    }
