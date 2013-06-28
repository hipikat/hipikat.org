
from hipikat.settings import settings_path


PROJECT_NAME = ADMINS = TIME_ZONE = LANGUAGE_CODE = None
SECRET_KEY = '12345'

# Include our sibling default settings.
execfile(settings_path.child('default.py'))
