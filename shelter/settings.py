"""
Django settings for Project project.

Generated by 'django-admin startproject' using Django 1.8.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd75_awn2qsnk!z*m)gdx(7^u1b4rqnn+pjoofg(4qa%^#bp&3w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['.shelter-associates.org']

# Application definition
INSTALLED_APPS = (
    'admin_view_permission',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
     #'south',
     'master',
     'component',
      #'Filter',
     'sponsor',
     'colorfield',
     'mastersheet',
     'graphs',
     'rest_framework',
     'rest_framework.authtoken',
     'rest_auth',
     'drf_dynamic_fields',
)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

ADMIN_VIEW_PERMISSION_MODELS = [
    'auth.User',
    'master.Survey',
    'master.Slum',
    'master.Rapid_Slum_Appraisal',
]

MIDDLEWARE = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'shelter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'shelter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
POSTGIS_VERSION = (2, 0, 3)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

from shelter.local_settings import *

STATIC_URL = '/static/'

SITE_URL = '/'

STATIC_ROOT = ''

STATICFILES_DIRS = (
   # Put strings here, like "/home/html/static" or "C:/www/django/static".
   # Always use forward slashes, even on Windows.
   # Don't forget to use absolute paths, not relative paths.
   os.path.join( BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

ADMIN_SITE_HEADER = "shelter Administration"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 

LOGIN_REDIRECT_URL = 'login_success'
