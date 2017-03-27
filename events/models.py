from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel

from cpm_generic.models import TranslatedField
from modeladminutils.edit_handlers import AdminModelChooserPanel
from submissions.constants import SECTIONS


class FilmProgramRelatedFilm(Orderable):

    page = ParentalKey('FilmProgram', related_name='related_films')
    film = models.ForeignKey(
        'cpm_data.Film',
        null=True,
        blank=True,
        related_name='+'
    )

    def get_country_display(self):
        return self.film.get_country_display()

    title = property(lambda self: self.film.title)
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
    ]


class FilmProgram(Page):

    section = models.IntegerField(choices=SECTIONS)

    name_en = models.CharField(max_length=1000)
    name_be = models.CharField(max_length=1000)
    name_ru = models.CharField(max_length=1000)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    description_en = RichTextField(default='')
    description_be = RichTextField(default='')
    description_ru = RichTextField(default='')
    description = TranslatedField('description_en',
                                  'description_be',
                                  'description_ru')

    content_panels = Page.content_panels + [
        FieldPanel('section'),
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('description_en'),
        FieldPanel('description_be'),
        FieldPanel('description_ru'),
        InlinePanel('related_films', label="Films"),
    ]


class Event(Page):

    starts_at = models.DateTimeField(db_index=True)
    program = models.ForeignKey(FilmProgram, null=True, blank=True,
                                on_delete=models.PROTECT)

    name_en = models.CharField(max_length=1000)
    name_be = models.CharField(max_length=1000)
    name_ru = models.CharField(max_length=1000)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    description_en = RichTextField(default='')
    description_be = RichTextField(default='')
    description_ru = RichTextField(default='')
    description = TranslatedField('description_en',
                                  'description_be',
                                  'description_ru')
    content_panels = Page.content_panels + [
        FieldPanel('starts_at'),
        FieldPanel('program'),
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('description_en'),
        FieldPanel('description_be'),
        FieldPanel('description_ru'),
    ]
