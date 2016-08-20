from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from cpm_generic.constants import COUNTRIES
from cpm_generic.models import TranslatedField


class JuryMember(models.Model):
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


class Partner(models.Model):
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


class Season(models.Model):
    name_en = models.CharField(max_length=250)
    name_be = models.CharField(max_length=250)
    name_ru = models.CharField(max_length=250)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
    ]
