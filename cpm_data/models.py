from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Orderable  # TODO: is this good?
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modeladminutils.edit_handlers import GenericModelChooserPanel
from cpm_generic.constants import COUNTRIES
from cpm_generic.models import TranslatedField

from cpm_data.queryset import SearchableQuerySet


class BaseSearchableManager(models.Manager):
    def get_queryset(self):
        return SearchableQuerySet(self.model)


SearchableManager = BaseSearchableManager.from_queryset(SearchableQuerySet)


class Film(index.Indexed, ClusterableModel):
    """Model representing accepted film

    Submissions contain raw data that need to be preprocessed/translated
    before publishing. This model contains all the data about an accepted
    submission that will be published.
    """
    submission = models.ForeignKey(
        'submissions.Submission',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    title_en = models.CharField(max_length=1000, default='', blank=True)
    title_be = models.CharField(max_length=1000, default='', blank=True)
    title_ru = models.CharField(max_length=1000, default='', blank=True)
    title = TranslatedField('title_en', 'title_be', 'title_ru')

    director_en = models.CharField(max_length=1000, default='', blank=True)
    director_be = models.CharField(max_length=1000, default='', blank=True)
    director_ru = models.CharField(max_length=1000, default='', blank=True)
    director = TranslatedField('director_en', 'director_be', 'director_ru')

    country = models.CharField(max_length=2, choices=COUNTRIES,
                               null=True, blank=True)

    city_en = models.CharField(max_length=100, default='', blank=True)
    city_be = models.CharField(max_length=100, default='', blank=True)
    city_ru = models.CharField(max_length=100, default='', blank=True)
    city = TranslatedField('city_en', 'city_be', 'city_ru')

    year = models.IntegerField(null=True, blank=True)

    duration_en = models.CharField(max_length=100, default='', blank=True)
    duration_be = models.CharField(max_length=100, default='', blank=True)
    duration_ru = models.CharField(max_length=100, default='', blank=True)
    duration = TranslatedField('duration_en', 'duration_be', 'duration_ru')

    genre_en = models.CharField(max_length=1000, default='', blank=True)
    genre_be = models.CharField(max_length=1000, default='', blank=True)
    genre_ru = models.CharField(max_length=1000, default='', blank=True)
    genre = TranslatedField('genre_en', 'genre_be', 'genre_ru')

    synopsis_short_en = RichTextField(default='', blank=True)
    synopsis_short_be = RichTextField(default='', blank=True)
    synopsis_short_ru = RichTextField(default='', blank=True)
    synopsis_short = TranslatedField('synopsis_short_en',
                                     'synopsis_short_be',
                                     'synopsis_short_ru')

    synopsis_en = RichTextField(default='', blank=True)
    synopsis_be = RichTextField(default='', blank=True)
    synopsis_ru = RichTextField(default='', blank=True)
    synopsis = TranslatedField('synopsis_en', 'synopsis_be', 'synopsis_ru')

    frame = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    objects = SearchableManager()

    def __unicode__(self):
        return u'"{}" / {}'.format(self.title, self.director)

    panels = [
        FieldPanel('submission'),
        FieldPanel('title_en'),
        FieldPanel('title_be'),
        FieldPanel('title_ru'),
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

    search_fields = [
        index.SearchField('title_en', partial_match=True, boost=2),
        index.SearchField('title_be', partial_match=True, boost=2),
        index.SearchField('title_ru', partial_match=True, boost=2),
        index.SearchField('director_en', partial_match=True, boost=2),
        index.SearchField('director_be', partial_match=True, boost=2),
        index.SearchField('director_ru', partial_match=True, boost=2),
        index.SearchField('synopsis_short_en', partial_match=True),
        index.SearchField('synopsis_short_be', partial_match=True),
        index.SearchField('synopsis_short_ru', partial_match=True),
        index.SearchField('synopsis_en', partial_match=True),
        index.SearchField('synopsis_be', partial_match=True),
        index.SearchField('synopsis_ru', partial_match=True),
    ]


class JuryMember(ClusterableModel):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    info_en = models.CharField(max_length=5000)
    info_be = models.CharField(max_length=5000)
    info_ru = models.CharField(max_length=5000)
    info = TranslatedField('info_en', 'info_be', 'info_ru')

    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    country = models.CharField(max_length=2, choices=COUNTRIES)

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        ImageChooserPanel('photo'),
        FieldPanel('country'),
        FieldPanel('info_en'),
        FieldPanel('info_be'),
        FieldPanel('info_ru'),
    ]


class SeasonRelatedJuryMember(Orderable):
    season = ParentalKey('Season', related_name='related_jury_members')
    jury_member = models.ForeignKey(
        'cpm_data.JuryMember',
        null=True,
        blank=True,
        related_name='+'
    )

    category_en = models.CharField(max_length=250, blank=True, default='')
    category_be = models.CharField(max_length=250, blank=True, default='')
    category_ru = models.CharField(max_length=250, blank=True, default='')
    category = TranslatedField('category_en', 'category_be', 'category_ru')

    name = property(lambda self: self.jury_member.name)
    info = property(lambda self: self.jury_member.info)
    photo = property(lambda self: self.jury_member.photo)
    country = property(lambda self: self.jury_member.country)

    panels = [
        GenericModelChooserPanel('jury_member'),
        FieldPanel('category_en'),
        FieldPanel('category_be'),
        FieldPanel('category_ru'),
    ]


class Partner(ClusterableModel):
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

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('link'),
        ImageChooserPanel('image'),
    ]


class SeasonRelatedPartner(Orderable):
    season = ParentalKey('Season', related_name='related_partners')
    partner = models.ForeignKey(
        'cpm_data.Partner',
        null=True,
        blank=True,
        related_name='+'
    )

    name = property(lambda self: self.partner.name)
    link = property(lambda self: self.partner.link)
    image = property(lambda self: self.partner.image)

    panels = [
        GenericModelChooserPanel('partner'),
    ]


class Season(ClusterableModel):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        InlinePanel('related_jury_members', label="Jury members"),
        InlinePanel('related_partners', label="Partners"),
    ]
