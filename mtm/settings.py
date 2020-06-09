"""
Django settings for mtm project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import os
import pytz
import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_FILE = '%s/auth/secret.txt' % BASE_DIR
with open(SECRET_KEY_FILE, 'r', encoding='utf8') as f:
    content = f.readline()
SECRET_KEY = content[:-1]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
]

if not DEBUG:
    ALLOWED_HOSTS += [
        'mtmchicago.com',
        'www.mtmchicago.com',
    ]


# Application definition

INSTALLED_APPS = [
    'home',
    'users',
    'locations',
    'events',
    'images',
    'articles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mtm.urls'

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

WSGI_APPLICATION = 'mtm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    PGPASSWORD_FILE = '%s/auth/.pgpass' % BASE_DIR
    with open(PGPASSWORD_FILE, 'r', encoding='utf8') as f:
        content = f.readline()
    PGPASSWORD = content[12:-1]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mtm',
            'USER': 'mtm',
            'PASSWORD': PGPASSWORD,
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Name for footers
NAME = 'Market to Market Chicago'


# PyTZ time zone
TZ = pytz.timezone(TIME_ZONE)


# Regular expressions
# EMAIL_REGEX = re.compile(
#     r'^[a-zA-Z0-9.!#$%&’*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'
# )
URL_REGEX = re.compile(
    r'^(?:(?:https?)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
)
HTTP_HTTPS_REGEX = re.compile(
    r'^https?://'
)
PHONE_REGEX = re.compile(
    r'^(\+?0?1\s)?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$'
)
PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()?])[A-Za-z\d!@#$%^&*()?]{8,}$'
)


# Google Maps API key
GOOGLE_MAPS_API_KEY_FILE = '%s/auth/google_maps_api_key.txt' % BASE_DIR
with open(GOOGLE_MAPS_API_KEY_FILE, 'r', encoding='utf8') as f:
    content = f.readline()
GOOGLE_MAPS_API_KEY = content[:-1]


# Page length for paginators
NEWS_ITEMS_PER_PAGE = 15


# Maximum number of invites at a time
MAX_INVITES = 20


# Domain name and protocol for invite URLs
if DEBUG:
    DOMAIN = 'http://10.0.0.100:8080'
else:
    DOMAIN = 'https://mtmchicago.com'


# Expiry duration for invites
INVITES_EXPIRY = datetime.timedelta(days=30)


