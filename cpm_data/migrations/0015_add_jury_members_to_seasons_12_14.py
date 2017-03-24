# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from django.db import migrations


def add_to_season(apps, schema_editor, season_name, jury_names):
    JuryMember = apps.get_model('cpm_data.JuryMember')
    Season = apps.get_model('cpm_data.Season')
    SeasonJuryMember = apps.get_model('cpm_data.SeasonRelatedJuryMember')

    season = Season.objects.get(name_en=season_name)

    for name in jury_names:
        try:
            jury_member = JuryMember.objects.get(name_en=name)
        except JuryMember.DoesNotExist:
            raise

        SeasonJuryMember.objects.get_or_create(season=season,
                                               jury_member=jury_member)


def remove_from_season(apps, schema_editor, season_name, jury_names):
    Season = apps.get_model('cpm_data.Season')
    SeasonJuryMember = apps.get_model('cpm_data.SeasonRelatedJuryMember')

    season = Season.objects.get(name_en=season_name)
    season_jury_members = SeasonJuryMember.objects.filter(
        season=season, jury_member__name_en__in=jury_names
    )

    season_jury_members.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0014_remove_jury_duplicates'),
    ]

    operations = [
        migrations.RunPython(
            partial(add_to_season,
                    season_name=season_name,
                    jury_names=jury_names),
            partial(remove_from_season,
                    season_name=season_name,
                    jury_names=jury_names),
        ) for season_name, jury_names in [
            ('2012', ['Agricola de Cologne', 'Victor Aslyuk', 'Maciej Gil',
                      'Pavel Ivanov', 'Yuri Igrusha', 'Andrew Kureichik',
                      'Sergey Krasikov', 'Bohdana Smirnova', 'Cory McAbee']),
            ('2013', ['Volha Dashuk', 'Irina Demyanova', 'Anton Sidorenko',
                      'Pavel Ivanov', 'Yuri Igrusha', 'Sergey Krasikov',
                      'Bohdana Smirnova', 'Jon Rubin', 'Maciej Gil',
                      'Pierre-Luc Vaillancourt', 'Karsten Weber',
                      'Lee Sang-woo', 'Cory McAbee']),
            ('2014', ['Yuri Igrusha']),  # more added in previous migrations
        ]
    ]
