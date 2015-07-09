"""
Django settings for the Hipikat.org project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os


# Absolute path to the checked-out repository - note the Python path is 'src/'
# (/...)  /[repository]   /src            /hipikat_org    /settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def set_setting(name, default=None, evaluate=False):
    """
    Set the setting `name` from an environment variable named `DJANGO_(name)`,
    if it exists, otherwise from the contents of `(BASE_DIR)/var/env/(name)`,
    if it exists.
    
    If `evaluate` is `True` or a value found in the environment or a file is
    equal to `'True'` or `'False'` (the strings), the value will be passed
    through `eval()`.

    If `default` is supplied and no matching environment variable or file is
    found, its value is used for the setting, and is unaffected by `evaluate`.
    """
    value = None
    envfile_path = os.path.join(BASE_DIR, 'var', 'env', name)

    if 'DJANGO_' + name in os.environ:
        value = os.environ['DJANGO_' + name]
    elif os.path.isfile(envfile_path):
        with open(envfile_path) as env_file:
            value = env_file.read()
    if evaluate or value in ('True', 'False'):
        value = eval(value)
    if value is None and default is not None:
        value = default
    if value is not None:
        globals()[name] = value

####
# Django settings
####

# Meta
ADMINS = (('Adam Wright', 'adam@hipikat.org'),)
TIME_ZONE = 'Australia/West'

# Security
ALLOWED_HOSTS = ['.hipikat.org', '.hpk.io']
set_setting('DEBUG', False)
set_setting('SECRET_KEY')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-au'
SHORT_DATE_FORMAT = 'Y-m-d'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Main system configuration
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'hipikat_org.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hipikat_org.wsgi.application'


# Database
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
