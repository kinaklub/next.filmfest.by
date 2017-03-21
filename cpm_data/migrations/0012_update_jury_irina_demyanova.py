# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def update_irina_demyanova(apps, schema_editor):
    JuryMember = apps.get_model('cpm_data.JuryMember')
    JuryMember.objects.filter(name_en='Irina Demyanova ').update(
        name_en='Irina Demyanova',
        country='BY',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0011_add_jury_data_to_season'),
    ]

    operations = [
        migrations.RunPython(
            update_irina_demyanova,
            lambda apps, scema_editor: None
        )
    ]
