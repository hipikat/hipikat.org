from .base import *

###
# Data storage and caching
###
DATABASES['default'].update({
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': DB_DIR.child('blank_slate.db'),
})
