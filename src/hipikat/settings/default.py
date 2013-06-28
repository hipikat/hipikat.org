
from hipikat.settings import settings_path


# Debugging and development modes
DEBUG = False

# Include our sibling base settings. (Note: this also sets s and g.)
execfile(settings_path.child('base.py'))

# Directory structure
s('MEDIA_ROOT', TMP_DIR.child('media'))

# Databases
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': DB_DIR.child('default.db')
}}
