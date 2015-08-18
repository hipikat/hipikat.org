"""
Django settings for the site at Hipikat.org

About: https://docs.djangoproject.com/en/1.8/topics/settings/
Reference: https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from functools import partial

from hipikat_org import BASE_DIR
from hipikat_org.util import env_setting


####
# Django settings
####

# Meta
ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
TIME_ZONE = 'Australia/West'

# Security
ALLOWED_HOSTS = ['.hipikat.org', '.hpk.io']
DEBUG = env_setting('DEBUG', False)
SECRET_KEY = env_setting('SECRET_KEY')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-au'
SHORT_DATE_FORMAT = 'Y-m-d'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Main system configuration
WSGI_APPLICATION = 'hipikat_org.wsgi.application'
ROOT_URLCONF = 'hipikat_org.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sekizai',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

# Databases
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'db', 'default.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
