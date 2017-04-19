# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


register = template.Library()


def get_mainmenu_items(lang):
    ff_prefix = 'http://filmfest.by/' + lang
    cpm_prefix = 'http://cpm.filmfest.by/' + lang
    return [
        (_('Home'), ff_prefix + '/', ()),
        (
            _('Festival'),
            '',
            (
                (_('2012: good memories'), ff_prefix + '/2012/'),
                (_('2013: good memories'), ff_prefix + '/2013/'),
                (_('Regulations'), ff_prefix + '/rules/'),
                (_('Submit your film!'), ff_prefix + '/submit/'),
            )
        ),
        (
            _('Volunteers'),
            '',
            (
                (_('Join in'), ff_prefix + '/vklyuchajsya/'),
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
            cpm_prefix + '/partners/',
            ()
        ),
        (
            _('Press-center'),
            '',
            (
                (_('Press-kit'), ff_prefix + '/press-kit/'),
                (_('Festival in media'), ff_prefix + '/media/'),
            )
        ),
        (
            _('Contacts'),
            ff_prefix + '/contact/',
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
