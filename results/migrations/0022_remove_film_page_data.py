# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def remove_film_pages(apps, schema_editor):
    FilmPage = apps.get_model('results.FilmPage')
    for film_page in FilmPage.objects.all():
        film_page.delete()


def remove_film_index(apps, schema_editor):
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    try:
        films_index = IndexPage.objects.get(slug='films')
    except IndexPage.DoesNotExist:
        pass
    else:
        films_index.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0021_drop_jurymemberpage'),
        ('cpm_generic', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_film_pages),
        migrations.RunPython(remove_film_index),
    ]
