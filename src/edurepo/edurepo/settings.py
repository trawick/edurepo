"""
Django settings for edurepo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import logging
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import stat

import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open('settings.cfg'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config.get('secret', 'key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('debugging', 'DEBUG') == 'True'
TEMPLATE_DEBUG = config.get('debugging', 'TEMPLATE_DEBUG') == 'True'
ALLOWED_HOSTS = [x for x in config.get('deployment', 'ALLOWED_HOSTS') if x != '']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'bootstrap3',
    'repo',
    'resources',
    'teachers',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'edurepo.urls'

WSGI_APPLICATION = 'edurepo.wsgi.application'

MOUNTED_AT = config.get('deployment', 'MOUNTED_AT')

LOGIN_URL = MOUNTED_AT + '/login/google/'

SOCIAL_AUTH_LOGIN_URL = '/login/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = <TBD>
# SOCIAL_AUTH_LOGIN_ERROR_URL = <TBD>
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('database', 'NAME'),
        'USER': config.get('database', 'USER'),
        'PASSWORD': config.get('database', 'PASSWORD'),
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TASTYPIE_DEFAULT_FORMATS = ['json']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

if config.get('deployment', 'set_static_root') == 'True':
    STATIC_ROOT = config.get('deployment', 'STATIC_ROOT')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LOG_DIRECTORY = config.get('logging', 'DIRECTORY')
GLOBAL_LOG_LEVEL = config.get('logging', 'GLOBAL_LEVEL')


def group_writable_file_handler(filename, mode='a', encoding=None):
    if not os.path.exists(filename):
        # We can only make it group writable if we are the owner.
        # We're always the owner if we create it, and that path
        # should be sufficient.
        open(filename, 'a').close()
        os_mode = os.stat(filename).st_mode
        os.chmod(filename, os_mode | stat.S_IWGRP)
    return logging.FileHandler(filename, mode, encoding)

LOGGING = {
    'version': 1,
    'disable_existing_logers': False,
    # what do the log records look like?
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    # what can we do with the log records?
    'handlers': {
        'file': {
            '()': group_writable_file_handler,
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIRECTORY, 'edjective.log'),
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        # catch-all logger:
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['file'],
            'level': GLOBAL_LOG_LEVEL,
        }
    }
}
