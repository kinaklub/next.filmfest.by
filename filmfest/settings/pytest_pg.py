from .pytest import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'filmfest',
        'USER': 'postgres',
    }
}
