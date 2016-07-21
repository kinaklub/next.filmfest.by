from .base import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

DEBUG = False
TEMPLATE_DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # noqa: F405
ALLOWED_HOSTS = ['next.filmfest.by']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),  # noqa: F405
        },
    },
}

STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'
