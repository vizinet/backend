"""
Django settings for AIRPACT_Fire project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url
from spirit.settings import *
# IF YOU WANT TO RUN THIS LOCALLY YOU MUST SET PRODUCTION TO 0
PRODUCTION = 0
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'et20@fybnrzon4b77v5yg*&19ozx*)#gpjhkly*u6u*52!x*1o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


INSTALLED_APPS.extend([
    'dal',
    'dal_select2',


    # custom apps
    'file_upload',
    'user_profile',
    'convos',

    # comment apps
    #'threadedcomments',
    'django.contrib.sites',
    'django_comments',
    'gunicorn',
    'storages'
    #'fluent_comments',
    #'crispy_forms',
])

AUTH_USER_MODEL = 'user_profile.AirpactUser'
SITE_ID = 1

MIDDLEWARE_CLASSES.extend( [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
])

ROOT_URLCONF = 'AIRPACT_Fire.urls'


PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


WSGI_APPLICATION = 'AIRPACT_Fire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/



# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# MEDIA_URL = '/media/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# STATIC_URL = '/static/'

AUTH_PROFILE_MODULE = 'user_profile.UserProfile'



LOGIN_REDIRECT_URL='/user/'
LOGIN_URL='/user/'
TIME_ZONE = "America/Los_Angeles"
USE_TZ = True

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


if PRODUCTION is 1:
    # AWS_STORAGE_BUCKET_NAME = 'airpactfire'
    # AWS_ACCESS_KEY_ID = 'AKIAJS7IVSXCUDE4GWVQ'
    # AWS_SECRET_ACCESS_KEY = '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'

    # # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # # We also use it in the next setting.
    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
    # # refers directly to STATIC_URL. So it's safest to always set it.
    # STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN

    # # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # # you run `collectstatic`).
    # STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


    # # STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]
    # MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT,'static')
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'))
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static/'), ]
