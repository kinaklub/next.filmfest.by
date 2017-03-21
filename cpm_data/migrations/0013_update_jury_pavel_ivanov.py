# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import migrations

from cpm_generic.migration_utils import get_image


def update_pavel_ivanov(apps, schema_editor):
    JuryMember = apps.get_model('cpm_data.JuryMember')

    try:
        pavel_ivanov = JuryMember.objects.get(name_en='Pavel Ivanov')
    except JuryMember.DoesNotExist:
        pass
    else:
        this_dir = os.path.dirname(__file__)
        filepath = os.path.join(this_dir, '0013', 'Pavel Ivanov.jpg')

        new_photo = get_image(apps, 'Pavel Ivanov', filepath)
        old_photo = pavel_ivanov.photo
        pavel_ivanov.photo = new_photo

        pavel_ivanov.save()
        if old_photo:
            old_photo.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0012_update_jury_irina_demyanova'),
    ]

    operations = [
        migrations.RunPython(
            update_pavel_ivanov,
            lambda apps, scema_editor: None
        )
    ]
