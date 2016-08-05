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


def get_jury_data():
    jury_json = os.path.join(
        MIGRATION_DIR,
        '0016_add_results_14_data/jury.json'
    )
    return json.load(open(jury_json, 'rb'), 'utf8')


def add_jury_member_pages(apps, schema_editor):
    Image = get_image_model(apps)
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    Collection = apps.get_model('wagtailcore.Collection')

    jury_member_page_ct = get_content_type(apps, 'results', 'jurymemberpage')

    collection_id = Collection.objects.filter(depth=1)[0]
    juryindex_page = IndexPage.objects.get(slug='jury')

    for item in get_jury_data():
        photo = Image(title=item['title'], collection=collection_id)

        photo_file = os.path.join(MIGRATION_DIR, item['photo'])
        photo.file.save(
            name=item['title'] + os.extsep + item['photo_ext'],
            content=File(open(photo_file, 'r'))
        )
        photo.save()

        slug = slugify(item['title'])
        add_subpage(
            parent=juryindex_page,
            model=JuryMemberPage,
            title=item['title'],
            slug=slug,
            name_en=item['name_en'],
            name_be=item['name_be'],
            name_ru=item['name_ru'],
            info_en=item['info_en'],
            info_be=item['info_be'],
            info_ru=item['info_ru'],
            country=item['country'],
            photo=photo,
            content_type=jury_member_page_ct,
        )


def _add_year_results(apps, page_kwargs, jury_members):
    HomePage = apps.get_model('home.HomePage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    RelatedJuryMember = apps.get_model('results.ResultsRelatedJuryMember')
    ResultsPage = apps.get_model('results.ResultsPage')

    results_page_ct = get_content_type(apps, 'results', 'resultspage')

    homepage = HomePage.objects.get(slug='home')
    year_results_page = add_subpage(
        homepage,
        ResultsPage,
        content_type=results_page_ct,
        **page_kwargs
    )

    RelatedJuryMember.objects.bulk_create(
        [
            RelatedJuryMember(
                sort_order=index,
                jury_member=JuryMemberPage.objects.get(title=title),
                page=year_results_page,
            ) for index, title in enumerate(jury_members)
        ]
    )


def _get_jurymember_kw(item):
    return {
        'title': item['title'],
        'slug': slugify(item['title']),
        'name_en': item['name_en'],
        'name_be': item['name_be'],
        'name_ru': item['name_ru'],
        'info_en': item['info_en'],
        'info_be': item['info_be'],
        'info_ru': item['info_ru'],
        'country': item['country'],
    }


def remove_jury_member_pages(apps, schema_editor):
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")

    jury_member_page_ct = get_content_type(apps, 'results', 'jurymemberpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    juryindex_page = IndexPage.objects.get(slug='jury')

    for item in get_jury_data():
        photo = Image.objects.get(title=item['title'],
                                  collection=collection_id)
        photo.delete()

        remove_subpage(
            parent=juryindex_page,
            model=JuryMemberPage,
            content_type=jury_member_page_ct,
            **_get_jurymember_kw(item)
        )


def add_results_2014(apps, schema_editor):
    _add_year_results(
        apps,
        dict(
            title=u'Results 2014',
            slug='results2014',
            caption_en='2014: good memories',
            caption_be='2014: добрыя ўспаміны',
            caption_ru='2014: хорошие воспоминания',
        ),
        [
            'Yuri Igrusha',
            'Valentyna Zalevska',
            'Goh Choon Ean',
            'Alexei Tutkin',
            'Carin Bräck',
            'Lidia Mikheeva',
            'Youlian Tabakov',
            'David Roberts',
            'Filmgruppe Chaos',
            'Pierre-Luc Vaillancourt - 2',
            'Christophe Beaucourt',
        ]
    )


def _remove_year_results(apps, page_kwargs, jury_members):
    HomePage = apps.get_model('home.HomePage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    RelatedJuryMember = apps.get_model('results.ResultsRelatedJuryMember')
    ResultsPage = apps.get_model('results.ResultsPage')

    results_page_ct = get_content_type(apps, 'results', 'resultspage')

    homepage = HomePage.objects.get(slug='home')
    results12_page = remove_subpage(
        homepage,
        ResultsPage,
        content_type=results_page_ct,
        **page_kwargs
    )

    related_jury_ids = chain.from_iterable(
        RelatedJuryMember.objects.filter(
            jury_member=JuryMemberPage.objects.get(title=title),
            page=results12_page,
        ).values_list('id', flat=True) for title in jury_members
    )
    RelatedJuryMember.objects.filter(id__in=related_jury_ids).delete()


def _get_data_2014():
    page_kwargs = dict(
        title=u'Results 2014',
        slug='results2014',
        caption_en='2014: good memories',
        caption_be='2014: добрыя ўспаміны',
        caption_ru='2014: хорошие воспоминания',
    )
    jury_members = [
        'Yuri Igrusha',
        'Valentyna Zalevska',
        'Goh Choon Ean',
        'Alexei Tutkin',
        'Carin Bräck',
        'Lidia Mikheeva',
        'Youlian Tabakov',
        'David Roberts',
        'Filmgruppe Chaos',
        'Pierre-Luc Vaillancourt - 2',
        'Christophe Beaucourt',
    ]
    return page_kwargs, jury_members


def remove_results_2014(apps, schema_editor):
    page_kwargs, jury_members = _get_data_2014()
    _remove_year_results(apps, page_kwargs, jury_members)


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0015_resultsrelatedpartner'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_jury_member_pages, remove_jury_member_pages),
        migrations.RunPython(add_results_2014, remove_results_2014),
    ]
