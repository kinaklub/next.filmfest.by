# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import json
from django.core.files import File
from django.db import migrations
from django.utils.text import slugify

from cpm_generic.migration_utils import (add_subpage, get_content_type,
                                         get_image_model)


def get_jury_data():
    json_path = os.path.join(os.path.dirname(__file__), '2014/jury.json')
    return json.load(open(json_path, 'rb'), 'utf8')

def add_jury_member_pages(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    Image = get_image_model(apps)
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    Collection = apps.get_model('wagtailcore.Collection')

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')
    jury_member_page_ct = get_content_type(apps, 'results', 'jurymemberpage')

    homepage = HomePage.objects.get(slug='home')
    collection_id = Collection.objects.filter(depth=1)[0]
    # import pdb; pdb.set_trace()
    juryindex_page = IndexPage.objects.get(slug='jury')

    for item in get_jury_data():
        photo = Image(title=item['title'], collection=collection_id)

        print os.path.abspath(item['photo'])
        photo_file = os.path.join(os.path.dirname(__file__), item['photo'])
        print photo_file
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
    results12_page = add_subpage(
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
                page=results12_page,
            ) for index, title in enumerate(jury_members)
        ]
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
            'Valentyna Zalevska',
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0014_partnerpage_link'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_jury_member_pages),
        migrations.RunPython(add_results_2014),
    ]
