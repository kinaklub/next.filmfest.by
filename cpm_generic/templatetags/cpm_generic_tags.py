import re

from django import template
from django.utils import translation
from django.conf import settings

from home.models import HomePage


register = template.Library()


@register.simple_tag
def rootpage():
    page = HomePage.objects.get(slug='home')
    return page


@register.inclusion_tag('cpm_generic/tags/mainmenu.html')
def mainmenu(request):
    curr_lang = translation.get_language().split('-')[0]
    full_path = request.get_full_path()
    match = re.match(r'^/%s(?P<path>/.*)$' % curr_lang, full_path)
    path = match.group('path') if match else full_path

    languages = [
        (
            code,
            name,
            '/%s%s' % (code, path),
            code == curr_lang
        ) for code, name in settings.LANGUAGES
    ]

    return {'languages': languages}
