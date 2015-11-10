from .base import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = False


try:
    from .local import *  # noqa
except ImportError:
    pass
