# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from cpm_generic.migration_utils import remove_subpage


def clear_jury_data(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model('results.JuryMemberPage')
    RelatedJuryMember = apps.get_model('results.ResultsRelatedJuryMember')

    homepage = HomePage.objects.get(slug='home')
    juryindex = IndexPage.objects.get(slug='jury')

    for obj in RelatedJuryMember.objects.all():
        obj.delete()

    for obj in JuryMemberPage.objects.all():
        obj.photo.delete()
        remove_subpage(
            parent=juryindex,
            model=JuryMemberPage,
            id=obj.id
        )

    remove_subpage(
        parent=homepage,
        model=IndexPage,
        id=juryindex.id
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0019_results_fk_season'),
    ]

    operations = [
        migrations.RunPython(
            clear_jury_data,
            lambda apps, scema_editor: None
        ),
    ]
