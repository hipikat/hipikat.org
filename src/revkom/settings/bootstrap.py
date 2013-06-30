
from revkom.settings import settings_path


PROJECT_NAME = 'revkom'
ADMINS = ()
SECRET_KEY = '12345'

# Include our sibling default settings.
execfile(settings_path.child('default.py'))

s('SECRET_KEY_FILE', CONF_DIR.child('SECRET_KEY'))
