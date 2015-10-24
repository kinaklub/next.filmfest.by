from django.utils.translation import ugettext_lazy as _

import pycountry


__all__ = ['YESNO', 'YESNOMAYBE', 'SECTIONS', 'BACKLINKS', 'LANGUAGES']


YESNO = (
    (1, _('Yes')),
    (2, _('No')),
)

YESNOMAYBE = (
    (0, _('Maybe')),
    (1, _('Yes')),
    (2, _('No')),
)

SECTIONS = (
    (1, _('Fiction')),
    (2, _('Animation')),
    (3, _('Documentary')),
    (4, _('Experimental')),
)

BACKLINKS = (
    (1, _('festival website')),
    (2, _('Facebook')),
    (3, _('Twitter')),
    (4, _('vk.com')),
    (5, _('email')),
    (6, _('internet search')),
    (7, _('friends')),
    (8, _('festivals database')),
    (9, _('I participated in CPM\'2012')),
    (10, _('place of study')),
    (11, _('work')),
    (12, _('other')),
)


LANGUAGES = sorted(
    (
        (lang.alpha2, _(lang.name))
        for lang in pycountry.languages
        if hasattr(lang, 'alpha2')
    ),
    key=lambda x: x[1]
)
