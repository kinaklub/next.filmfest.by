from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from cpm_generic.models import TranslatedField
from modeladminutils.edit_handlers import AdminModelChooserPanel


class ResultsRelatedWinner(Orderable):
    page = ParentalKey('ResultsPage', related_name='related_winners')
    film = models.ForeignKey(
        'cpm_data.Film',
        null=False,
        blank=False,
        related_name='+'
    )

    nomination_en = models.CharField(max_length=250, blank=True, default='')
    nomination_be = models.CharField(max_length=250, blank=True, default='')
    nomination_ru = models.CharField(max_length=250, blank=True, default='')
    nomination = TranslatedField('nomination_en',
                                 'nomination_be',
                                 'nomination_ru')

    film_title = property(lambda self: self.film.title)
    director = property(lambda self: self.film.director)
    country = property(lambda self: self.film.country)
    city = property(lambda self: self.film.city)
    year = property(lambda self: self.film.year)
    duration = property(lambda self: self.film.duration)
    genre = property(lambda self: self.film.genre)
    synopsis_short = property(lambda self: self.film.synopsis_short)
    synopsis = property(lambda self: self.film.synopsis)
    frame = property(lambda self: self.film.frame)

    panels = [
        AdminModelChooserPanel('film'),
        FieldPanel('nomination_en'),
        FieldPanel('nomination_be'),
        FieldPanel('nomination_ru'),
    ]


class ResultsFact(Orderable):

    class Position(object):
        TOP = 't'
        BOTTOM = 'b'

        DEFAULT = BOTTOM
        CHOICES = [
            (TOP, _(u'Top')),
            (BOTTOM, _(u'Bottom')),
        ]

    page = ParentalKey('ResultsPage', related_name='related_facts')

    number = models.CharField(max_length=10, default='')

    caption_en = models.CharField(max_length=100, default='')
    position_en = models.CharField(max_length=1, choices=Position.CHOICES,
                                   default=Position.DEFAULT)

    caption_be = models.CharField(max_length=100, default='')
    position_be = models.CharField(max_length=1, choices=Position.CHOICES,
                                   default=Position.DEFAULT)

    caption_ru = models.CharField(max_length=100, default='')
    position_ru = models.CharField(max_length=1, choices=Position.CHOICES,
                                   default=Position.DEFAULT)

    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')
    position = TranslatedField('position_en', 'position_be', 'position_ru')


class PartnerPage(Page):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    link = models.CharField(max_length=250, blank=True, default='')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('link'),
        ImageChooserPanel('image'),
    ]


class ResultsRelatedPartner(Orderable):
    page = ParentalKey('ResultsPage', related_name='related_partners')
    partner = models.ForeignKey(
        'results.PartnerPage',
        null=True,
        blank=True,
        related_name='+'
    )

    name = property(lambda self: self.partner.name)
    link = property(lambda self: self.partner.link)
    image = property(lambda self: self.partner.image)

    panels = [
        PageChooserPanel('partner'),
    ]


class ResultsPage(Page):
    season = models.ForeignKey(
        'cpm_data.Season',
        null=False,
        blank=False,
        related_name='+'
    )
    caption_en = models.CharField(max_length=250)
    caption_be = models.CharField(max_length=250)
    caption_ru = models.CharField(max_length=250)
    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')

    content_panels = Page.content_panels + [
        FieldPanel('season'),
        FieldPanel('caption_en'),
        FieldPanel('caption_be'),
        FieldPanel('caption_ru'),
        # InlinePanel('nomination_films', label="Nominations"),
        # seems that we can have two or more different nomination
        # for the same film
        InlinePanel('related_winners', label="Winners"),
        InlinePanel('related_facts', label="Facts"),
        InlinePanel('related_partners', label="Partners"),
    ]
