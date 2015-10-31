from django.db import models
from django.utils import translation

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class TranslatedField(object):
    def __init__(self, en_field, be_field, ru_field):
        self.en_field = en_field
        self.be_field = be_field
        self.ru_field = ru_field

    def __get__(self, instance, owner):
        fields = {
            'en': self.en_field,
            'be': self.be_field,
            'ru': self.ru_field,
        }
        field = fields[translation.get_language()]
        return getattr(instance, field)


class IndexPage(Page):
    caption_en = models.CharField(max_length=250)
    caption_be = models.CharField(max_length=250)
    caption_ru = models.CharField(max_length=250)
    caption = TranslatedField('caption_en', 'caption_be', 'caption_ru')

    description_en = RichTextField(default='')
    description_be = RichTextField(default='')
    description_ru = RichTextField(default='')
    description = TranslatedField('description_en',
                                  'description_be',
                                  'description_ru')

    content_panels = Page.content_panels + [
        FieldPanel('caption_en'),
        FieldPanel('caption_be'),
        FieldPanel('caption_ru'),
        FieldPanel('description_en'),
        FieldPanel('description_be'),
        FieldPanel('description_ru'),
    ]
