# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


register = template.Library()


def get_mainmenu_items(lang):
    prefix = 'http://filmfest.by/' + lang
    return [
        (_('Home'), prefix + '/', ()),
        (
            _('Festival'),
            '',
            (
                (_('2012: good memories'), prefix + '/2012/'),
                (_('2013: good memories'), prefix + '/2013/'),
                (_('Regulations'), prefix + '/rules/'),
                (_('Submit your film!'), prefix + '/submit/'),
            )
        ),
        (
            _('Volunteers'),
            '',
            (
                (_('Join in'), prefix + '/vklyuchajsya/'),
                (
                    _('Discussion group'),
                    'http://groups.google.com/group/cpm2015'
                ),
                (
                    _('Volunteer form'),
                    'http://filmfest.by/ru/2013/page/volunteer_form'
                )
            )
        ),
        (
            _('Partners'),
            prefix + '/cpm/partners/',
            ()
        ),
        (
            _('Press-center'),
            '',
            (
                (_('Press-kit'), prefix + '/press-kit/'),
                (_('Festival in media'), prefix + '/media/'),
            )
        ),
        (
            _('Contacts'),
            prefix + '/contact/',
            ()
        ),
    ]


@register.inclusion_tag('cpm_compat/tags/mainmenu.html')
def mainmenu_compat(request):
    cur_lang = translation.get_language().split('-')[0]

    parts = request.get_full_path().split('/', 2)
    path = parts[2] if len(parts) > 2 else ''

    languages = [
        (
            code,
            name,
            '/%s/%s' % (code, path),
            code == cur_lang
        ) for code, name in [
            ('en', u'English'),
            ('ru', u'Русский'),
            ('be', u'Беларуская'),
        ]
    ]

    return {
        'mainmenu_items': get_mainmenu_items(cur_lang),
        'languages': languages,
    }
