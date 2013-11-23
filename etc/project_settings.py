
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

ROOT_FQDN = 'hipikat.org'
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'

DATABASES = { 
    'default': {
        'USER': 'hipikat',
        'NAME': 'hipikat.org',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PASSWORD': 'insecure',
    }   
}  

PYTHON_VERSION = '2.7.6'

PROJECT_NAME = 'hipikat.org'
PROJECT_GIT_URL = 'git@github.com:hipikat/hipikat.org.git'
PROJECT_SHARED_SECRET = os.path.join(DIRS.ETC_DIR, 'shared_secret_rsa')
PROJECT_SHARED_SECRET_PUB = PROJECT_SHARED_SECRET + '.pub'
PROJECT_LIBS = { 
    'django-cinch': 'git@github.com:hipikat/django-cinch.git',
    'django-revkom': 'git@github.com:hipikat/django-revkom.git',
    'django-scow': 'git@github.com:hipikat/django-scow.git',
    'feincms-elephantblog': 'git@github.com:hipikat/feincms-elephantblog.git',
}


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
