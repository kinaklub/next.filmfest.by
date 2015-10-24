from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from cpm_generic.constants import COUNTRIES

from cpm_generic.models import TranslatedField


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

    panels = [
        PageChooserPanel('jury_member'),
    ]


class ResultsPage(Page):
    caption_en = models.CharField(max_length=250)
    caption_be = models.CharField(max_length=250)
    caption_ru = models.CharField(max_length=250)
    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')

    content_panels = Page.content_panels + [
        FieldPanel('caption_en'),
        FieldPanel('caption_be'),
        FieldPanel('caption_ru'),
        InlinePanel('related_jury_members', label="Jury members"),
    ]
