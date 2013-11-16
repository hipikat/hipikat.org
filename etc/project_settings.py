
import os
from os.path import dirname
from revkom.utils import find_public_ssh_keys

ADMINS = [{
    'full_name': 'Adam Wright',
    'username': 'hipikat',
    'email': 'adam@hipikat.org',
}]
ALLOWED_HOSTS = ['.hipikat.org']
APP_OWNER = 'hipikat'
BASE_DIR = dirname(dirname(__file__))        # [repo]/etc/project_settings.py
LANGUAGE_CODE = 'en-au'
PROJECT_NAME = 'hipikat.org'
PYTHON_VERSION = '2.7.6'
TIME_ZONE = 'Australia/Perth'
