# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from dateutil.parser import parse as parse_datetime
from django.conf import settings
from django.db import migrations

from cpm_generic.migration_utils import (add_subpage, get_content_type,
                                         remove_subpage)


DATA_DIR = os.path.join(os.path.dirname(__file__), '0004')
TIMETABLE_TITLE = 'Timetable'


def _get_data(filename):
    with open(os.path.join(DATA_DIR, filename)) as data_file:
        return json.load(data_file)


def add_filmprograms_2017(apps, schema_editor):
    FilmProgram = apps.get_model('events.FilmProgram')
    filmprogram_ct = get_content_type(apps, 'events', 'filmprogram')

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    for item in _get_data('filmprograms.json'):
        if not FilmProgram.objects.filter(title=item['title']).exists():
            add_subpage(
                parent=homepage,
                model=FilmProgram,
                content_type=filmprogram_ct,
                live=True,
                **item
            )


def remove_filmprograms_2017(apps, schema_editor):
    FilmProgram = apps.get_model('events.FilmProgram')

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    for item in _get_data('filmprograms.json'):
        if FilmProgram.objects.filter(title=item['title']).exists():
            remove_subpage(
                parent=homepage,
                model=FilmProgram,
                title=item['title'],
            )


def add_venues_2017(apps, schema_editor):
    Venue = apps.get_model('events.Venue')

    for item in _get_data('venues.json'):
        if not Venue.objects.filter(name_en=item['name_en']).exists():
            Venue(**item).save()


def remove_venues_2017(apps, schema_editor):
    Venue = apps.get_model('events.Venue')

    for item in _get_data('venues.json'):
        try:
            program = Venue.objects.get(name_en=item['name_en'])
        except Venue.DoesNotExist:
            pass
        else:
            program.delete()


def add_timetable_2017(apps, schema_editor):
    FilmProgram = apps.get_model('events.FilmProgram')
    TimeTable = apps.get_model('events.TimeTable')
    TimeTableEvent = apps.get_model('events.TimeTableEvent')
    Venue = apps.get_model('events.Venue')

    timetable_ct = get_content_type(apps, 'events', 'timetable')

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    if TimeTable.objects.filter(title=TIMETABLE_TITLE).exists():
        return

    timetable = add_subpage(
        parent=homepage,
        model=TimeTable,
        title=TIMETABLE_TITLE,
        content_type=timetable_ct,
        caption_en='Timetable',
        caption_be='Расклад',
        caption_ru='Расписание',
        slug='2017-timetable',
        live=True,
    )
    for item in _get_data('events.json'):
        TimeTableEvent(
            page=timetable,
            program=FilmProgram.objects.get(title=item['program']),
            venue=Venue.objects.get(name_en=item['venue']),
            starts_at=parse_datetime(item['starts_at']),
        ).save()


def remove_timetable_2017(apps, schema_editor):
    TimeTable = apps.get_model('events.TimeTable')

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    remove_subpage(
        parent=homepage,
        model=TimeTable,
        title=TIMETABLE_TITLE,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_add_timetable_model'),
        ('home', '0002_create_homepage'),
    ]

    if settings.DEVELOPMENT:
        operations = [
            migrations.RunPython(add_filmprograms_2017,
                                 remove_filmprograms_2017),
            migrations.RunPython(add_venues_2017, remove_venues_2017),
            migrations.RunPython(add_timetable_2017, remove_timetable_2017),
        ]
    else:
        operations = []
