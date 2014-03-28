"""
Django settings for sds project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'AKIAJQNKLMGJLI4CHBNQ'
EMAIL_HOST_PASSWORD = 'AtfCX9kdOOsS4pHqHKMzQG0/eyTmqBrz92L6XbA0oiEB'
EMAIL_USE_TLS = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAIC27KBAMV4JLB2CQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'silentdiscosquad'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p*n^r53fg(-$u+d5fr+0qr%4xxo6()r^77y%wki$u3#+1i!a@8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'sds',
    'south',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sds.urls'

WSGI_APPLICATION = 'sds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sdsdev',
        'USER': 'rdsuser',
        'PASSWORD': 'dancefloor04',
        'HOST': 'sdsdev.c1u3oij6dqlo.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = ( "/home/ec2-user/sds/templates",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ec2-user/sds/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ec2-user/sds/media/'


STATICFILES_DIRS = (
    "/home/ec2-user/sds/sds/templates/static/", "/home/ec2-user/sds/static/",
)

