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
DIR_0017 = os.path.join(MIGRATION_DIR, '0018_add_partners_2012_data')


# TODO: coulds be abstracted
def get_partners_2012_data():
    partners_json = os.path.join(
        MIGRATION_DIR,
        '0018_add_partners_2012_data/partners.json'
    )
    return json.load(open(partners_json, 'rb'), 'utf8')


def _get_partnerindex_kw():
    return {
        'title': u'Partners',
        'slug': 'Partners',
        'caption_en': u'Partners',
        'caption_be': u'Партнёры',
        'caption_ru': u'Партнеры',
        'description_en': u'List of CPM partners for all times',
        'description_be': u'Список партнеров CPM на все времена',
        'description_ru': u'Спіс партнёраў CPM на ўсе часы',
    }


def get_parner_image(apps, item):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')

    collection_id = Collection.objects.filter(depth=1)[0]

    title = slugify(item['name_en'])

    frame = Image(title=title, collection=collection_id)

    photo_file = os.path.join(DIR_0017, item['image'])
    frame.file.save(
        name=title + os.extsep + '.jpg',
        content=File(open(photo_file, 'rb'))
    )
    return frame


def create_partner_index_page(apps):
    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')

    IndexPage = apps.get_model('cpm_generic.IndexPage')
    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')
    partnerindex_page = add_subpage(
        parent=homepage,
        model=IndexPage,
        content_type=index_page_ct,
        **_get_partnerindex_kw()
    )

    return partnerindex_page


def create_partner_pages(apps):
    parnerindex_page = create_partner_index_page(apps)

    ParnerPage = apps.get_model("results.PartnerPage")
    partner_page_ct = get_content_type(apps, 'results', 'partnerpage')
    pages = []
    for item in get_partners_2012_data():
        image = get_parner_image(apps, item)
        image.save()

        slug = slugify(item['id'])
        title = item['name_en']
        page = add_subpage(
            parent=parnerindex_page,
            model=ParnerPage,
            title=title,
            slug=slug,
            name_en=item['name_en'],
            name_be=item['name_be'],
            name_ru=item['name_ru'],
            link=item['link'],
            image=image,
            content_type=partner_page_ct,
        )

        pages.append(page)

    return pages


def get_results_page(apps):
    ResultsPage = apps.get_model('results.ResultsPage')
    results2012_page = ResultsPage.objects.get(slug='results2012')

    return results2012_page


def add_patners_pages(apps, schema_editor):
    pages = create_partner_pages(apps)

    results2012_page = get_results_page(apps)

    ResultsRelatedPartner = apps.get_model('results.ResultsRelatedPartner')

    epages = enumerate(pages)
    ResultsRelatedPartner.objects.bulk_create(
        [
            ResultsRelatedPartner(
                sort_order=index,
                partner=partner,
                page=results2012_page,
            ) for index, partner in epages
        ]
    )


def _get_partner_kw(item):
    return {
        'title': item['name_en'],
        'slug': slugify(item['id']),
    }


def remove_partners_pages(apps, schema_editor):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    PartnerPage = apps.get_model("results.PartnerPage")
    ResultsRelatedPartner = apps.get_model('results.ResultsRelatedPartner')

    partner_page_ct = get_content_type(apps, 'results', 'partnerpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    HomePage = apps.get_model('home.HomePage')
    homepage = HomePage.objects.get(slug='home')

    IndexPage = apps.get_model('cpm_generic.IndexPage')
    partnersindex_page = IndexPage.objects.get(slug='Partners')
    partners_data = get_partners_2012_data()

    results2012_page = get_results_page(apps)

    related_film_ids = chain.from_iterable(
        ResultsRelatedPartner.objects.filter(
            partner=PartnerPage.objects.filter(title=item['name_en']),
            page=results2012_page,
        ).values_list('id', flat=True) for item in partners_data
    )

    ResultsRelatedPartner.objects.filter(id__in=related_film_ids).delete()

    for item in partners_data:
        title = slugify(item['name_en'])
        photo = Image.objects.get(title=title,
                                  collection=collection_id)
        photo.delete()

        remove_subpage(
            parent=partnersindex_page,
            model=PartnerPage,
            content_type=partner_page_ct,
            **_get_partner_kw(item)
        )

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')
    remove_subpage(
        homepage,
        IndexPage,
        content_type=index_page_ct,
        slug='Partners',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0017_add_films_2012_data'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_patners_pages, remove_partners_pages),
    ]
