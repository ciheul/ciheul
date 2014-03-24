# Django settings for ciheul project.

import os
import sys
import socket
import config
from datetime import timedelta
#from common import get_ip_port

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# add project path to python path
DJANGO_ROOT = os.path.realpath('')
PROJECT_PATH = os.path.join(DJANGO_ROOT, 'ciheul')
sys.path += [PROJECT_PATH]

# get ip address and port.
#IP_ADDRESS, PORT = get_ip_port()

ADMINS = (
    ('Winnu Ayi Satria', 'winnuayi@gmail.com'),
    ('Galih Kanigoro', 'galih.kanigoro@gmail.com'),
)

MANAGERS = ADMINS

IP_ADDR = socket.gethostbyname(socket.gethostname())

DATABASES = {
    'default': {
        'ENGINE': config.ENGINE,
        'NAME': config.DB,
        'USER': config.USER,
        'PASSWORD': config.PASS,
        'HOST': config.HOST,
        'PORT': config.PORT,
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Jakarta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static/img/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/static/img/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''
#STATIC_ROOT = os.path.join(DJANGO_ROOT, 'ciheul/static/')
#STATIC_ROOT = '/Users/winnuayi/Projects/dev/www/ciheul/ciheul/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    #os.path.join(DJANGO_ROOT, 'ciheul/static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8_^4a0sfg=+8iz9nb18jpo&p6frq^cy*e9f%p03shx6=g%^d9i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ciheul.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ciheul.wsgi.application'

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'bootstrap_toolkit',
    # ciheul apps
    'ciheul',
    'bigear',
    'bigdrive',
    'dirban',
    'bigpath', 
    'juara',
    'jendela24',
    'south',
    # third plugin
    'tastypie',
    'social_auth',
    'registration',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

APPEND_SLASH = False

# django-tastypie
TASTYPIE_DEFAULT_FORMATS = ['json']

# django-social-auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dirban/members/'
LOGIN_ERROR_URL = '/login-error/'

AUTHENTICATION_BACKENDS = {
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
}

TEMPLATE_CONTEXT_PROCESSORS = {
    'social_auth.context_processors.social_auth_by_type_backends',
    'django.contrib.auth.context_processors.auth',
}

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = {'twitter'}

TWITTER_CONSUMER_KEY = config.CONSUMER_KEY
TWITTER_CONSUMER_SECRET = config.CONSUMER_SECRET

BROKER_URL='amqp://'
CELERY_RESULT_BACKEND = 'redis://'

CELERYBEAT_SCHEDULE = {
    'fetch-rss-every-10-minutes': {
        'task': 'jendela24.celery.fetch_rss',
        'schedule': timedelta(minutes=5),
        #'schedule': timedelta(minutes=1),
        #'schedule': timedelta(seconds=15),
    },        
}
