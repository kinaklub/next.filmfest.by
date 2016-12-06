from .base import *  # noqa


INSTALLED_APPS.append('wagtail.tests.testapp')  # noqa: F405


SECRET_KEY = 'test'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),  # noqa: F405
    }
}


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db',
    }
}
