from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from cpm_generic.constants import COUNTRIES

from cpm_generic.models import TranslatedField

# partners - links, banner, name
# places - link, addr, name, photo, coord ([lng, lat])


class FilmPage(Page):
    submission = models.ForeignKey(
        'submissions.Submission',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    film_title_en = models.CharField(max_length=1000, default='')
    film_title_be = models.CharField(max_length=1000, default='')
    film_title_ru = models.CharField(max_length=1000, default='')
    film_title = TranslatedField('film_title_en',
                                 'film_title_be',
                                 'film_title_ru')

    director_en = models.CharField(max_length=1000, default='')
    director_be = models.CharField(max_length=1000, default='')
    director_ru = models.CharField(max_length=1000, default='')
    director = TranslatedField('director_en', 'director_be', 'director_ru')

    country = models.CharField(max_length=2, choices=COUNTRIES)

    city_en = models.CharField(max_length=100, default='')
    city_be = models.CharField(max_length=100, default='')
    city_ru = models.CharField(max_length=100, default='')
    city = TranslatedField('city_en', 'city_be', 'city_ru')

    year = models.IntegerField()

    duration_en = models.CharField(max_length=100, default='')
    duration_be = models.CharField(max_length=100, default='')
    duration_ru = models.CharField(max_length=100, default='')
    duration = TranslatedField('duration_en', 'duration_be', 'duration_ru')

    genre_en = models.CharField(max_length=1000, default='')
    genre_be = models.CharField(max_length=1000, default='')
    genre_ru = models.CharField(max_length=1000, default='')
    genre = TranslatedField('genre_en', 'genre_be', 'genre_ru')

    synopsis_short_en = RichTextField(default='')
    synopsis_short_be = RichTextField(default='')
    synopsis_short_ru = RichTextField(default='')
    synopsis_short = TranslatedField('synopsis_short_en',
                                     'synopsis_short_be',
                                     'synopsis_short_ru')

    synopsis_en = RichTextField(default='')
    synopsis_be = RichTextField(default='')
    synopsis_ru = RichTextField(default='')
    synopsis = TranslatedField('synopsis_en', 'synopsis_be', 'synopsis_ru')

    frame = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # film.nomination
    # year
    # country
    # duration if possible to automate generate 12 min to edit inline?
    # is it good idea?

    content_panels = Page.content_panels + [
        FieldPanel('submission'),
        FieldPanel('film_title_en'),
        FieldPanel('film_title_be'),
        FieldPanel('film_title_ru'),
        FieldPanel('director_en'),
        FieldPanel('director_be'),
        FieldPanel('director_ru'),
        FieldPanel('country'),
        FieldPanel('city_en'),
        FieldPanel('city_be'),
        FieldPanel('city_ru'),
        FieldPanel('genre_en'),
        FieldPanel('genre_be'),
        FieldPanel('genre_ru'),
        FieldPanel('year'),
        FieldPanel('duration_en'),
        FieldPanel('duration_be'),
        FieldPanel('duration_ru'),
        FieldPanel('synopsis_short_en'),
        FieldPanel('synopsis_short_be'),
        FieldPanel('synopsis_short_ru'),
        FieldPanel('synopsis_en'),
        FieldPanel('synopsis_be'),
        FieldPanel('synopsis_ru'),
        ImageChooserPanel('frame'),
    ]


class JuryMemberPage(Page):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    info_en = models.CharField(max_length=1000)
    info_be = models.CharField(max_length=1000)
    info_ru = models.CharField(max_length=1000)
    info = TranslatedField('info_en', 'info_be', 'info_ru')

    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    country = models.CharField(max_length=2, choices=COUNTRIES)

    content_panels = Page.content_panels + [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        ImageChooserPanel('photo'),
        FieldPanel('country'),
        FieldPanel('info_en'),
        FieldPanel('info_be'),
        FieldPanel('info_ru'),
    ]


class ResultsRelatedJuryMember(Orderable):
    page = ParentalKey('ResultsPage', related_name='related_jury_members')
    jury_member = models.ForeignKey(
        'results.JuryMemberPage',
        null=True,
        blank=True,
        related_name='+'
    )

    name = property(lambda self: self.jury_member.name)
    info = property(lambda self: self.jury_member.info)
    photo = property(lambda self: self.jury_member.photo)
    country = property(lambda self: self.jury_member.country)
    slug = property(lambda self: self.jury_member.slug)

    panels = [
        PageChooserPanel('jury_member'),
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


class ResultsPage(Page):
    caption_en = models.CharField(max_length=250)
    caption_be = models.CharField(max_length=250)
    caption_ru = models.CharField(max_length=250)
    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')

    content_panels = Page.content_panels + [
        FieldPanel('caption_en'),
        FieldPanel('caption_be'),
        FieldPanel('caption_ru'),
        # InlinePanel('nomination_films', label="Nominations"),
        # seems that we can have two or more different nomination
        # for the same film
        InlinePanel('related_facts', label="Facts"),
        InlinePanel('related_jury_members', label="Jury members"),
    ]


class PartnerPage(Page):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

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
        ImageChooserPanel('image'),
    ]
