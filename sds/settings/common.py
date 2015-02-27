# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path
import json

#used in emails from myauth dir
#SITE_IP_OR_DOMAIN = "54.173.157.204"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOUTH_TESTS_MIGRATE = False

ACCOUNT_AUTHENTICATION_METHOD = ("username_email")
ACCOUNT_EMAIL_REQUIRED = (True)
AUTH_PROFILE_MODULE = 'sds.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
    #zinia context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'zinnia.context_processors.version',  # Optionl
    'django.contrib.messages.context_processors.messages',
)

FIXTURE_DIRS = (
   'sds/fixtures/sds_testdata.json',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 465
HOSTNAME = "54.173.157.204"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'us@silentdiscosquad.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'silentdiscosquad'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_HEADERS = {
    'Content-Disposition': 'attachment'
    }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 
COMPRESS_ENABLED = False
ALLOWED_HOSTS = ['*']
TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'sds',
    'south',
    'django_extensions',
    'mailchimp',
    'compressor',
    'django.contrib.comments',
    'tagging',
    'mptt',
    'zinnia',
    'myauth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'sds.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TEMPLATE_DIRS = ( "/home/ec2-user/sds/templates",)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATIC_URL = '/static/'
STATIC_ROOT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ec2-user/sds/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

AUTH_USER_MODEL = 'myauth.User'

ZINNIA_SPAM_CHECKER_BACKENDS = ('zinnia_akismet.akismet', 'zinnia.spam_checker.backends.automattic', 'zinnia.spam_checker.backends.typepad','zinnia.spam_checker.backends.all_is_spam',)
AKISMET_API_KEY = '197e10c1c2ca'

DEV_DATABASE={
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "newdb",
        "USER": "martin",
        "PASSWORD": "dancefloor04",
        "HOST": "dev.cdadlb7rfieo.us-east-1.rds.amazonaws.com",
        "PORT": "5432"
    }
}

PREPROD_DATABASE={
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "newdb",
        "USER": "martin",
        "PASSWORD": "dancefloor04",
        "HOST": "preprod.cdadlb7rfieo.us-east-1.rds.amazonaws.com",
        "PORT": "5432"
    }
}

PRODUCTION_DATABASE={
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "newdb",
        "USER": "martin",
        "PASSWORD": "dancefloor04",
        "HOST": "sdslivefeb2.cdadlb7rfieo.us-east-1.rds.amazonaws.com",
        "PORT": "5432"
    }
}