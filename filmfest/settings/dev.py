from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJANGO_TEMPLATES['OPTIONS']['debug'] = True  # noqa: F405
INSTALLED_APPS.append('debug_toolbar')  # noqa: F405

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=bi%8p-j&&y5%4h8^oq-%(b@p&&wyu72b7qk4dlyvwo)!)wn20'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Enables /admin/styleguide/ route (Menu -> Settings -> Styleguide)
INSTALLED_APPS.append('wagtail.contrib.wagtailstyleguide')  # noqa: F405


try:
    from .local import *  # noqa
except ImportError:
    pass
