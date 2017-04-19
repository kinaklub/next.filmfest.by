import os


COMPAT_MODE_HOST = os.environ.get('COMPAT_MODE_HOST', 'cpm.filmfest.by')


def compat_mode(request):
    return {'in_compat_mode': request.get_host() == COMPAT_MODE_HOST}
