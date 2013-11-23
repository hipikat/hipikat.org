
import getpass
from glob import glob
import os
from os import path
#from cinch import cinch_settings
#from revkom.mixins import FHSDirsMixin
from cinch.utils import FHSDirs


BASE_DIR = path.dirname(path.dirname(__file__))        # [repo]/etc/project_settings.py
DIRS = FHSDirs(BASE_DIR)

ADMINS = [{
    'username': 'hipikat',
    'full_name': 'Adam Wright',
    'email': 'adam@hipikat.org',
    'shell': '/bin/bash',
    'skeleton_dir': os.path.join(DIRS.ETC_DIR, 'skel-hipikat'),
    'ssh_public_keys': [os.path.join(DIRS.ETC_DIR , 'ssh_public_keys', 'trepp_rsa.pub')],
    'requires_deb_packages': ('screen', 'mosh'),
}]
ALLOWED_HOSTS = ['.hipikat.org']
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'

PYTHON_VERSION = '2.7.6'

PROJECT_NAME = 'hipikat.org'
PROJECT_GIT_URL = 'git@github.com:hipikat/hipikat.org.git'

# TODO: Migrate this functionality to some generic scow.utils function
try:
    with open(path.join(DIRS.ETC_LOCAL_DIR, 'USER')) as fab_user_f:
        FABRIC_USER = fab_user_f.read()
except IOError as ex:
    # Only if the file isn't found; if it's not readable or something, we
    # should re-raise the exception
    import errno
    if ex.errno == errno.ENOENT:
        FABRIC_USER = getpass.getuser()
    else:
        raise
