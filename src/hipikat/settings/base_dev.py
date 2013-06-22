
from .common import project_settings


DEBUG = True
DEVELOP = True

# Push settings defined so far onto the project_settings singleton
project_settings.update(globals())
# Load base project settings
from .base import *
