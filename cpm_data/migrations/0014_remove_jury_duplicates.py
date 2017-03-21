# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def remove_duplicate_jury_members(apps, schema_editor):
    jury_names = [
        "Irina Demyanova",
        "Carin Bräck",
        "Pierre-Luc Vaillancourt",
    ]

    JuryMember = apps.get_model('cpm_data.JuryMember')
    SeasonJuryMember = apps.get_model('cpm_data.SeasonRelatedJuryMember')

    for name in jury_names:
        jury_members = JuryMember.objects.filter(name_en=name).order_by('id')
        original = jury_members[0]
        duplicates = jury_members[1:]
        for duplicate in duplicates:
            qs = SeasonJuryMember.objects.filter(jury_member=duplicate)
            qs.update(jury_member=original)
            duplicate.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0013_update_jury_pavel_ivanov'),
    ]

    operations = [
        migrations.RunPython(
            remove_duplicate_jury_members,
            lambda apps, scema_editor: None
        )
    ]
