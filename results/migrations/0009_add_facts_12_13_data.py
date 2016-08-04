# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain
import json
import os

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


def _remove_year_facts(apps, slug, facts):
    ResultsFact = apps.get_model('results.ResultsFact')
    ResultsPage = apps.get_model('results.ResultsPage')

    page = ResultsPage.objects.get(slug=slug)

    ids = chain.from_iterable(
        ResultsFact.objects.filter(
            number=fact['number'],
            caption_en=fact['caption_en'],
            position_en=fact['position_en'],
            caption_be=fact['caption_be'],
            position_be=fact['position_be'],
            caption_ru=fact['caption_ru'],
            position_ru=fact['position_ru'],
            page=page,
        ).values_list('id', flat=True) for fact in facts
    )
    ResultsFact.objects.filter(id__in=ids).delete()


def _get_data(filename):
    this_dir = os.path.dirname(__file__)
    path = os.path.join(this_dir, '0009', filename)

    with open(path) as data_file:
        return json.load(data_file)


def add_facts_2012(apps, schema_editor):
    _add_year_facts(
        apps,
        'results2012',
        _get_data('facts2012.json'),
    )


def remove_facts_2012(apps, schema_editor):
    _remove_year_facts(
        apps,
        'results2012',
        _get_data('facts2012.json'),
    )


def add_facts_2013(apps, schema_editor):
    _add_year_facts(
        apps,
        'results2013',
        _get_data('facts2013.json'),
    )


def remove_facts_2013(apps, schema_editor):
    _remove_year_facts(
        apps,
        'results2013',
        _get_data('facts2013.json'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_add_related_fact_model'),
    ]

    operations = [
        migrations.RunPython(add_facts_2012, remove_facts_2012),
        migrations.RunPython(add_facts_2013, remove_facts_2013),
    ]
