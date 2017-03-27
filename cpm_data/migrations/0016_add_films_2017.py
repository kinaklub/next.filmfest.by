# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.core.files import File
from django.db import migrations

from cpm_generic.migration_utils import get_image_model


DATA_DIR = os.path.join(os.path.dirname(__file__), '0016')


def _get_data():
    with open(os.path.join(DATA_DIR, 'films.json')) as data_file:
        return json.load(data_file)


def add_films_2017(apps, schema_editor):
    Film = apps.get_model('cpm_data.Film')
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')

    collection_id = Collection.objects.filter(depth=1)[0]

    for film_data in _get_data():

        if Film.objects.filter(title_en=film_data['title_en']).exists():
            continue

        frame = Image(title=film_data['title_en'], collection=collection_id)
        with open(os.path.join(DATA_DIR, film_data['frame']), 'rb') as frame_f:
            frame.file.save(name=film_data['frame'], content=File(frame_f))
            frame.save()

        film_data = film_data.copy()
        film_data.pop('frame')
        Film(frame=frame, **film_data).save()


def remove_films_2017(apps, schema_editor):
    Film = apps.get_model('cpm_data.Film')

    for film in _get_data():
        try:
            film = Film.objects.get(title_en=film['title_en'])
        except Film.DoesNotExist:
            pass
        else:
            film.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0015_add_jury_members_to_seasons_12_14'),
    ]

    operations = [
        migrations.RunPython(add_films_2017, remove_films_2017),
    ]
