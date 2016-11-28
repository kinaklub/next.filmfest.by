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


def get_nominations():
    nomination_json = os.path.join(
        MIGRATION_DIR,
        '0017_add_films_2012_data/nominations2012.json'
    )
    return json.load(open(nomination_json, 'rb'), 'utf8')


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


def create_film_index_page(apps):
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

    return filmsindex_page


def create_film_pages(apps):
    filmsindex_page = create_film_index_page(apps)

    FilmPage = apps.get_model("results.FilmPage")
    film_page_ct = get_content_type(apps, 'results', 'filmpage')
    nominations = get_nominations()
    pages = []
    for item in get_films_2012_data():
        frame = get_film_frame(apps, item)
        frame.save()

        slug = slugify(item['film_title_en'])
        print slug
        title = item['film_title_en']
        page = add_subpage(
            parent=filmsindex_page,
            model=FilmPage,
            title=title,
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
            duration_en=item['duration_en'],
            duration_ru=item['duration_ru'],
            duration_be=item['duration_be'],
            city_en=item['city_en'],
            city_ru=item['city_ru'],
            city_be=item['city_be'],
            year=item['year'],
            country=item['country'],

            frame=frame,
            content_type=film_page_ct,
        )
        nomination = next((n for n in nominations if n['film'] == title), 'None')


        pages.append({
            'p': page,
            'n': nomination,
        })

    return pages


def get_results_page(apps):
    ResultsPage = apps.get_model('results.ResultsPage')
    results2012_page = ResultsPage.objects.get(slug='results2012')

    return results2012_page


def add_films_pages(apps, schema_editor):
    pages = create_film_pages(apps)

    results2012_page = get_results_page(apps)

    ResultsRelatedWinner = apps.get_model('results.ResultsRelatedWinner')

    #from pdb import set_trace; set_trace()
    ResultsRelatedWinner.objects.bulk_create(
        [
            ResultsRelatedWinner(
                sort_order=index,
                film=film['p'],
                nomination_en=film['n'],
                nomination_ru='Perpetuum Mobile',
                nomination_be='Perpetuum Mobile',
                page=results2012_page,
            ) for index, film in enumerate(pages) if (film != 'None')
        ]
    )


def _get_film_kw(item):
    return {
        'title': item['film_title_en'],
        'slug': slugify(item['film_title_en']),
    }


def remove_films_pages(apps, schema_editor):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    FilmPage = apps.get_model("results.FilmPage")
    ResultsRelatedWinner = apps.get_model('results.ResultsRelatedWinner')

    film_page_ct = get_content_type(apps, 'results', 'filmpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    IndexPage = apps.get_model('cpm_generic.IndexPage')
    filmsindex_page = IndexPage.objects.get(slug='films')
    films2012_data = get_films_2012_data()

    results2012_page = get_results_page(apps)

    related_film_ids = chain.from_iterable(
        ResultsRelatedWinner.objects.filter(
            film=FilmPage.objects.filter(title=item['film_title_en']),
            page=results2012_page,
        ).values_list('id', flat=True) for item in films2012_data
    )

    ResultsRelatedWinner.objects.filter(id__in=related_film_ids).delete()

    for item in films2012_data:
        title = slugify(item['film_title_en'])
        photo = Image.objects.get(title=title,
                                  collection=collection_id)
        photo.delete()

        remove_subpage(
            parent=filmsindex_page,
            model=FilmPage,
            content_type=film_page_ct,
            **_get_film_kw(item)
        )

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')
    remove_subpage(
        homepage,
        IndexPage,
        content_type=index_page_ct,
        slug='films',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0016_add_results_14_data'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_films_pages, remove_films_pages),
    ]
