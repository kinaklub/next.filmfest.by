from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailcore.models import Orderable  # TODO: is this good?
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from cpm_generic.constants import COUNTRIES
from cpm_generic.models import TranslatedField


class JuryMember(ClusterableModel):
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
    page = ParentalKey('Season', related_name='related_jury_members')
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
        PageChooserPanel('jury_member'),
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

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('link'),
        ImageChooserPanel('image'),
    ]


class SeasonRelatedPartner(Orderable):
    page = ParentalKey('Season', related_name='related_partners')
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
        PageChooserPanel('partner'),
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
