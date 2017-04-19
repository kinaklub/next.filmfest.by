from __future__ import absolute_import, unicode_literals

import json

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.widgets import AdminChooser
from wagtail.contrib.modeladmin.helpers import AdminURLHelper

from modeladminutils.helpers import get_edit_url


class AdminModelChooser(AdminChooser):

    def __init__(self, model, **kwargs):
        self.target_model = model
        name = self.target_model._meta.verbose_name
        self.choose_one_text = _('Choose %s') % name
        self.choose_another_text = _('Choose another %s') % name
        self.link_to_chosen_text = _('Edit this %s') % name

        self.url_helper = AdminURLHelper(model)

        super(AdminModelChooser, self).__init__(**kwargs)

    def render_html(self, name, value, attrs):
        obj, value = self.get_instance_and_id(self.target_model, value)

        super_self = super(AdminModelChooser, self)
        original_field_html = super_self.render_html(name, value, attrs)
        edit_link = get_edit_url(self.target_model, obj.id) if obj else None

        return render_to_string(
            "modeladminutils/widgets/adminmodel_chooser.html",
            {
                'widget': self,
                'model_opts': self.target_model._meta,
                'original_field_html': original_field_html,
                'attrs': attrs,
                'value': value,
                'item': obj,
                'edit_link': edit_link,
            }
        )

    def render_js_init(self, id_, name, value):
        model = self.target_model

        return "createAdminModelChooser({id}, {model});".format(
            id=json.dumps(id_),
            model=json.dumps('{app}/{model}'.format(
                app=model._meta.app_label,
                model=model._meta.model_name)))
