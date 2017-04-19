from .base import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': '{}db'.format(STACK_PREFIX),  # noqa: F405
        'PORT': '5432',
    }
}

DEBUG = False
DEVELOPMENT = False
TEMPLATE_DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secret')  # noqa: F405
ALLOWED_HOSTS = (
    os.environ.get('DJANGO_ALLOWED_HOSTS', 'next.filmfest.by')  # noqa: F405
).split(',')

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
