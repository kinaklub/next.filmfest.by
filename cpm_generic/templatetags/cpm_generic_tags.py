
from django import template
from django.utils import translation
from django.conf import settings

from home.models import HomePage


register = template.Library()


def get_root_page():
    return HomePage.objects.get(slug='home')


def get_language_paths(full_path):
    curr_lang = translation.get_language().split('-')[0]
    urlang = '/%s/' % curr_lang
    path = full_path
    if path.startswith(urlang):
        path = path[len(urlang):]

    return [
        (
            code,
            name,
            '/%s/%s' % (code, path),
            code == curr_lang
        ) for code, name in settings.LANGUAGES
    ]


@register.inclusion_tag('cpm_generic/tags/mainmenu.html')
def mainmenu(request):
    full_path = request.get_full_path()
    return {'languages': get_language_paths(full_path),
            'rootpage': get_root_page()}
