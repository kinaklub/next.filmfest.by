# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import json
from itertools import chain

from django.core.files import File
from django.db import migrations
from django.utils.text import slugify

from cpm_generic.migration_utils import (add_subpage, get_content_type,
                                         get_image_model, remove_subpage)

MIGRATION_DIR = os.path.dirname(__file__)
DIR_0017 = os.path.join(MIGRATION_DIR, '0017_add_films_2012_data')


# TODO: coulds be abstracted
def get_films_2012_data():
    films_json = os.path.join(
        MIGRATION_DIR,
        '0017_add_films_2012_data/films2012.json'
    )
    return json.load(open(films_json, 'rb'), 'utf8')


def _get_filmsindex_kw():
    return {
        'title': u'Films',
        'slug': 'films',
        'caption_en': u'Films',
        'caption_be': u'Фільмы',
        'caption_ru': u'Фильмы',
        'description_en': u'List of CPM films for all times',
        'description_be': u'Список фильмов CPM на все времена',
        'description_ru': u'Спіс фільмаў CPM на ўсе часы',
    }


def get_film_frame(apps, item):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')

    collection_id = Collection.objects.filter(depth=1)[0]

    title = slugify(item['film_title_en'])

    frame = Image(title=title, collection=collection_id)

    photo_file = os.path.join(DIR_0017, item['frame'])
    frame.file.save(
        name=title + os.extsep + '.jpg',
        content=File(open(photo_file, 'rb'))
    )
    return frame


def add_films_pages(apps, schema_editor):
    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')

    IndexPage = apps.get_model('cpm_generic.IndexPage')
    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')
    filmsindex_page = add_subpage(
        parent=homepage,
        model=IndexPage,
        content_type=index_page_ct,
        **_get_filmsindex_kw()
    )

    FilmPage = apps.get_model("results.FilmPage")
    film_page_ct = get_content_type(apps, 'results', 'filmpage')
    for item in get_films_2012_data():
        frame = get_film_frame(apps, item)
        frame.save()

        slug = slugify(item['film_title_en'])
        add_subpage(
            parent=filmsindex_page,
            model=FilmPage,
            title=item['film_title_en'],
            slug=slug,
            film_title_en=item['film_title_en'],
            film_title_ru=item['film_title_ru'],
            film_title_be=item['film_title_be'],
            director_en=item['director_en'],
            director_ru=item['director_ru'],
            director_be=item['director_be'],
            genre_en=item['genre_en'],
            genre_ru=item['genre_ru'],
            genre_be=item['genre_be'],
            synopsis_en=item['synopsis_en'],
            synopsis_ru=item['synopsis_ru'],
            synopsis_be=item['synopsis_be'],
            year=item['year'],
            frame=frame,
            content_type=film_page_ct,
        )


def _get_film_kw(item):
    return {
        'title': item['film_title_en'],
        'slug': slugify(item['film_title_en']),
    }


def remove_films_pages(apps, schema_editor):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    FilmPage = apps.get_model("results.FilmPage")

    jury_member_page_ct = get_content_type(apps, 'results', 'filmpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    filmsindex_page = IndexPage.objects.get(slug='films')

    for item in get_films_2012_data():
        title = slugify(item['film_title_en'])
        photo = Image.objects.get(title=title,
                                  collection=collection_id)
        photo.delete()

        remove_subpage(
            parent=filmsindex_page,
            model=FilmPage,
            content_type=jury_member_page_ct,
            **_get_film_kw(item)
        )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0016_add_results_14_data'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_films_pages, remove_films_pages),
    ]
