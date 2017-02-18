from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel

from modeladminutils.widgets import GenericModelChooser


class BaseGenericModelChooserPanel(BaseChooserPanel):
    object_type_name = 'item'

    _target_model = None
    url_helper_class = None

    @classmethod
    def widget_overrides(cls):
        chooser = GenericModelChooser(model=cls.target_model(),
                                      url_helper_class=cls.url_helper_class)
        return {cls.field_name: chooser}

    @classmethod
    def target_model(cls):
        if cls._target_model is None:
            meta = cls.model._meta
            cls._target_model = meta.get_field(cls.field_name).rel.model

        return cls._target_model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            self.object_type_name: instance_obj,
        }))


class GenericModelChooserPanel(object):
    def __init__(self, field_name, url_helper_class=None):
        self.field_name = field_name
        self.url_helper_class = url_helper_class

    def bind_to_model(self, model):
        return type(
            str('_GenericModelChooserPanel'),
            (BaseGenericModelChooserPanel,),
            {
                'model': model,
                'field_name': self.field_name,
                'url_helper_class': self.url_helper_class,
            }
        )
