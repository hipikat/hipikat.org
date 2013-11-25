
import getpass
#from glob import glob
import os
from os import environ, path
from textwrap import dedent
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
    'ssh_public_keys': [os.path.join(DIRS.ETC_DIR, 'ssh_public_keys', 'trepp_rsa.pub')],
    'requires_deb_packages': ('screen', 'mosh'),
    'post_create': dedent("""
        git config --global core.excludesfile '~/.gitignore_global'
        git config --global user.email "adam@hipikat.org"
        git config --global user.name "Adam Wright"
        git config --global color.ui true
    """),
}]

ROOT_FQDN = 'hipikat.org'
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'


REQUIRE_DEB_PACKAGES = (
    'bundler',
    'unzip',
)

PYTHON_VERSION = '2.7.6'

PROJECT_NAME = 'hipikat.org'
PROJECT_GIT_URL = 'https://github.com/hipikat/hipikat.org.git'
PROJECT_SHARED_SECRET = os.path.join(DIRS.ETC_DIR, 'shared_secret_rsa')
PROJECT_SHARED_SECRET_PUB = PROJECT_SHARED_SECRET + '.pub'
PROJECT_LIBS = {
    'django-cinch': 'https://github.com/hipikat/django-cinch.git',
    'django-revkom': 'https://github.com/hipikat/django-revkom.git',
    'django-scow': 'https://github.com/hipikat/django-scow.git',
    'feincms-elephantblog': 'https://github.com/hipikat/feincms-elephantblog.git',
    #'zurb-foundation': 'git@github.com:zurb/foundation.git'
    'zurb-foundation': 'https://github.com/zurb/foundation.git'
}
PROJECT_MODULE = 'hipikat'
WSGI_APP_MODULE = PROJECT_MODULE + '.wsgi'


POST_INSTALL = dedent(r"""
    (cd src/styles && bundle install)
    rm -f $VIRTUAL_ENV/bin/postactivate
    cp {prj_postactivate} $VIRTUAL_ENV/bin/postactivate
    python scripts/make_secret_key.py > var/env/DJANGO_SECRET_KEY
    """.format(prj_postactivate="`cat $VIRTUAL_ENV/$VIRTUALENVWRAPPER_PROJECT_FILENAME`"
               "/scripts/export_env.sh"))

DATABASES = {
    'default': {
        'USER': 'hipikat',
        'NAME': PROJECT_NAME,
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PASSWORD': 'insecure',
    }
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
