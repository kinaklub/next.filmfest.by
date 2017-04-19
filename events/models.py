from __future__ import unicode_literals

from collections import defaultdict

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsearch import index

from cpm_generic.models import TranslatedField
from modeladminutils.edit_handlers import AdminModelChooserPanel
from modeladminutils.models import SearchableManager
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

    # TODO: add season
    # TODO: need remove section as required property
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


class Venue(index.Indexed, ClusterableModel):
    name_en = models.CharField(max_length=1000)
    name_be = models.CharField(max_length=1000)
    name_ru = models.CharField(max_length=1000)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    address_en = models.CharField(max_length=1000)
    address_be = models.CharField(max_length=1000)
    address_ru = models.CharField(max_length=1000)
    address = TranslatedField('address_en', 'address_be', 'address_ru')

    objects = SearchableManager()

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('address_en'),
        FieldPanel('address_be'),
        FieldPanel('address_ru'),
    ]


class TimeTableEvent(Orderable):

    page = ParentalKey('TimeTable', related_name='related_events')
    program = models.ForeignKey(FilmProgram, null=True, blank=True,
                                related_name='+')
    starts_at = models.DateTimeField(db_index=True)
    venue = models.ForeignKey(Venue, null=True, blank=True, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('program'),
        FieldPanel('starts_at'),
        AdminModelChooserPanel('venue'),
    ]


class TimeTable(Page):

    # TODO: add season
    caption_en = models.CharField(max_length=250)
    caption_be = models.CharField(max_length=250)
    caption_ru = models.CharField(max_length=250)
    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')

    content_panels = Page.content_panels + [
        FieldPanel('caption_en'),
        FieldPanel('caption_be'),
        FieldPanel('caption_ru'),
        InlinePanel('related_events', label="Events"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(TimeTable, self).get_context(request, *args, **kwargs)

        grouped_events = defaultdict(list)
        for event in self.related_events.all():
            group_key = event.starts_at.date()
            grouped_events[group_key].append(event)
        context['grouped_events'] = sorted(grouped_events.iteritems())

        is_legacy = bool(request.GET.get('legacy'))
        context['base_template'] = 'empty.html' if is_legacy else 'base.html'

        return context

    def serve(self, *args, **kwargs):
        """Serve page on new and legacy website"""
        response = super(TimeTable, self).serve(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
