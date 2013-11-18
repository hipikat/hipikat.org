
from glob import glob
import os
from os.path import dirname

BASE_DIR = dirname(dirname(__file__))        # [repo]/etc/project_settings.py

ADMINS = [{
    'full_name': 'Adam Wright',
    'username': 'hipikat',
    'email': 'adam@hipikat.org',
    'ssh_public_keys': [os.path.join(BASE_DIR, 'etc', 'ssh_public_keys', 'trepp_rsa.pub')],
    'shell': '/bin/bash',
    'skeleton_dir': os.path.join(BASE_DIR, 'etc', 'skel-hipikat')
}]
ALLOWED_HOSTS = ['.hipikat.org']
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Perth'

PYTHON_VERSION = '2.7.6'
PROJECT_NAME = 'hipikat.org'
PROJECT_GIT_URL = 'git@github.com:hipikat/hipikat.org.git'
