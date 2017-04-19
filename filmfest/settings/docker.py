from .dev import *  # noqa


INSTALLED_APPS.append('wagtail_pgsearchbackend')  # noqa: F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail_pgsearchbackend.backend',
        'SEARCH_CONFIG': 'english'
    }
}

STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'
