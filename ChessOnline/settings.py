"""
Django settings for ChessOnline project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from urllib.parse import urlparse
import os
import djcelery # Import Django-celery

djcelery.setup_loader()

#redis_url = urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_5uzsq8^jv4k+saz423p*51boisa99r1m#db^26d8wr3od%rwb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'Chess',
    'djcelery',
    'channels'
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]


ROOT_URLCONF = 'ChessOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Chess.templates')],
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

WSGI_APPLICATION = 'ChessOnline.wsgi.application'
AUTH_USER_MODEL = 'Chess.User'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
       # 'ENGINE': 'django.db.backends.sqlite3',
     #   'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd97n9475cn88jr',
        'USER' : 'rjklbnedpbyjup',
        'PASSWORD' : '66ad9e30e78c6edd129eb8f9320e408e4d357ccd06854cc81a4bd44fc5d7552b',
        'HOST' : 'ec2-54-247-166-129.eu-west-1.compute.amazonaws.com',
        'PORT' : '5432',

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Channels settings



CHANNEL_LAYERS = {
   "default": {
       "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
       "CONFIG": {
        "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # set redis address
          #"hosts": [os.environ.get('REDIS_URL', redis_url)],  # set redis address

       },
       "ROUTING": "Chess.routing.channel_routing",  # load routing from our routing.py file
   },
}

# Celery settings

# use json format for everything
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

'redis://localhost:6379'

CELERY_TASK_RESULT_EXPIRES = 10
CELERND_TASK_ERROR_EMAILS = False
CELERY_RESULT_BACKEND = "redis"
BROKER_URL = 'redis://localhost:6379/0'  # our redis address

#CELERY_REDIS_HOST = redis_url.hostname
CELERY_REDIS_HOST = 'localhost'
CELERY_REDIS_PORT = '6379'
CELERY_REDIS_DB = 1
#BROKER_URL = redis_url # our redis address


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        #'LOCATION': '/var/run/redis/redis.sock',
        'LOCATION': '%redis://localhost:6379'# % (redis_url.hostname, redis_url.port)
         ,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'}
           # 'PASSWORD': redis_url.password,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "Chess/static"),

]