
from .common import project_settings


###
# Security
###
SECRET_KEY = 'TODO: Insecure default secret key'


# Push settings defined so far onto the project_settings singleton
project_settings.update(globals())
# Load base project settings
from .base import *


###
# Data storage and caching
###
DATABASES['default'].update({
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': DB_DIR.child('blank_slate.db'),
})
