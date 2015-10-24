from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJANGO_TEMPLATES['DEBUG'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=bi%8p-j&&y5%4h8^oq-%(b@p&&wyu72b7qk4dlyvwo)!)wn20'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *  # noqa
except ImportError:
    pass
