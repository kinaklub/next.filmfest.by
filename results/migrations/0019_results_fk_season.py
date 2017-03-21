# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def migrate_existing_result_pages(apps, schema_editor):
    ResultsPage = apps.get_model('results.ResultsPage')
    Season = apps.get_model('cpm_data.Season')

    for result_page_title, season_name in [
            ('Results 2012', '2012'),
            ('Results 2013', '2013'),
            ('Results 2014', '2014'),
    ]:
        try:
            season = Season.objects.get(name_en=season_name)
        except Season.DoesNotExist:
            continue

        result_qs = ResultsPage.objects.filter(title=result_page_title)
        result_qs.update(season=season)


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0015_add_jury_members_to_seasons_12_14'),
        ('results', '0018_add_partners_2012_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultspage',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cpm_data.Season'),  # noqa: disable=E501
        ),
        migrations.RunPython(
            migrate_existing_result_pages,
            lambda apps, scema_editor: None
        ),
        migrations.AlterField(
            model_name='resultspage',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cpm_data.Season'),  # noqa: disable=E501
        ),
    ]
