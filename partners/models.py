from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page

# Create your models here.
from cpm_data.models import Season
from cpm_generic.models import TranslatedField
from modeladminutils.edit_handlers import AdminModelChooserPanel


class PartnersPage(Page):
    name_en = models.CharField(max_length=1000)
    name_be = models.CharField(max_length=1000)
    name_ru = models.CharField(max_length=1000)
    name = TranslatedField('name_en', 'name_be', 'name_ru')

    entry_en = RichTextField(default='')
    entry_be = RichTextField(default='')
    entry_ru = RichTextField(default='')
    entry = TranslatedField(
        'entry_en',
        'entry_be',
        'entry_ru'
    )

    season = models.ForeignKey(
        'cpm_data.Season',
        null=False,
        blank=False,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name_en'),
        FieldPanel('name_be'),
        FieldPanel('name_ru'),
        FieldPanel('entry_en'),
        FieldPanel('entry_be'),
        FieldPanel('entry_ru'),
        FieldPanel('season')
    ]
