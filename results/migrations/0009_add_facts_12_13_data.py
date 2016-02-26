# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def _add_year_facts(apps, slug, facts):
    ResultsFact = apps.get_model('results.ResultsFact')
    ResultsPage = apps.get_model('results.ResultsPage')

    page = ResultsPage.objects.get(slug=slug)

    ResultsFact.objects.bulk_create(
        [
            ResultsFact(
                sort_order=index,
                number=fact['number'],
                caption_en=fact['caption_en'],
                position_en=fact['position_en'],
                caption_be=fact['caption_be'],
                position_be=fact['position_be'],
                caption_ru=fact['caption_ru'],
                position_ru=fact['position_ru'],
                page=page,
            ) for index, fact in enumerate(facts)
        ]
    )


def add_facts_2012(apps, schema_editor):
    data = [
        {
            'number': u'2012',
            'caption_en': u'january',
            'position_en': u'b',
            'caption_be': u'студзень',
            'position_be': u'b',
            'caption_ru': u'январь',
            'position_ru': u'b',
        },
        {
            'number': u'7',
            'caption_en': u'days',
            'position_en': u'b',
            'caption_be': u'дзён',
            'position_be': u'b',
            'caption_ru': u'дней',
            'position_ru': u'b',
        },
        {
            'number': u'35',
            'caption_en': u'countries',
            'position_en': u'b',
            'caption_be': u'краіны',
            'position_be': u'b',
            'caption_ru': u'стран',
            'position_ru': u'b',
        },
        {
            'number': u'197',
            'caption_en': u'participants',
            'position_en': u'b',
            'caption_be': u'удзельнікаў',
            'position_be': u'b',
            'caption_ru': u'участников',
            'position_ru': u'b',
        },
        {
            'number': u'$0',
            'caption_en': u'budget',
            'position_en': u't',
            'caption_be': u'бюджэт',
            'position_be': u't',
            'caption_ru': u'бюджет',
            'position_ru': u't',
        },
        {
            'number': u'9',
            'caption_en': u'jury members',
            'position_en': u'b',
            'caption_be': u'членаў журы',
            'position_be': u'b',
            'caption_ru': u'членов жюри',
            'position_ru': u'b',
        },
        {
            'number': u'42',
            'caption_en': u'volunteers',
            'position_en': u'b',
            'caption_be': u'валанцёра',
            'position_be': u'b',
            'caption_ru': u'волонтера',
            'position_ru': u'b',
        },
    ]
    _add_year_facts(
        apps,
        'results2012',
        data
    )


def add_facts_2013(apps, schema_editor):
    data = [
        {
            'number': u'2013',
            'caption_en': u'january',
            'position_en': u'b',
            'caption_be': u'студзень',
            'position_be': u'b',
            'caption_ru': u'январь',
            'position_ru': u'b',
        },
        {
            'number': u'8',
            'caption_en': u'days',
            'position_en': u'b',
            'caption_be': u'дзён',
            'position_be': u'b',
            'caption_ru': u'дней',
            'position_ru': u'b',
        },
        {
            'number': u'42',
            'caption_en': u'countries',
            'position_en': u'b',
            'caption_be': u'краіны',
            'position_be': u'b',
            'caption_ru': u'стран',
            'position_ru': u'b',
        },
        {
            'number': u'320',
            'caption_en': u'participants',
            'position_en': u'b',
            'caption_be': u'удзельнікаў',
            'position_be': u'b',
            'caption_ru': u'участников',
            'position_ru': u'b',
        },
        {
            'number': u'$500',
            'caption_en': u'budget',
            'position_en': u't',
            'caption_be': u'бюджэт',
            'position_be': u't',
            'caption_ru': u'бюджет',
            'position_ru': u't',
        },
        {
            'number': u'9',
            'caption_en': u'jury members',
            'position_en': u'b',
            'caption_be': u'членаў журы',
            'position_be': u'b',
            'caption_ru': u'членов жюри',
            'position_ru': u'b',
        },
        {
            'number': u'150',
            'caption_en': u'volunteers',
            'position_en': u'b',
            'caption_be': u'валанцёраў',
            'position_be': u'b',
            'caption_ru': u'волонтеров',
            'position_ru': u'b',
        },
        {
            'number': u'8',
            'caption_en': u'showing stages',
            'position_en': u'b',
            'caption_be': u'пляцовак',
            'position_be': u'b',
            'caption_ru': u'площадок',
            'position_ru': u'b',
        },
        {
            'number': u'15',
            'caption_en': u'coutries participated in international screenings',
            'position_en': u'b',
            'caption_be': u'краін-удзельнікаў міжнародных паказаў ',
            'position_be': u'b',
            'caption_ru': u'стран-участников междунарожных показов',
            'position_ru': u'b',
        },
    ]
    _add_year_facts(
        apps,
        'results2013',
        data
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_add_related_fact_model'),
    ]

    operations = [
        migrations.RunPython(add_facts_2012),
        migrations.RunPython(add_facts_2013),
    ]
