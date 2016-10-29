# -*- coding: utf-8 -*-
import json
import os

from django.core.files import File
from django.db import migrations
from django.utils.text import slugify

from cpm_generic.migration_utils import (add_subpage, remove_subpage,
                                         get_content_type, get_image_model)


DIR_0005 = os.path.join(os.path.dirname(__file__), '0005')


def _get_data():
    with open(os.path.join(DIR_0005, 'data.json')) as data_file:
        return json.load(data_file)


def _get_photo_path(filename):
    return os.path.join(DIR_0005, 'photo', filename)


def _get_juryindex_kw():
    return {
        'title': u'Jury',
        'slug': 'jury',
        'caption_en': u'Jury',
        'caption_be': u'Журы',
        'caption_ru': u'Жюри',
        'description_en': u'List of CPM jury members for all times',
        'description_be': u'Список членов жюри CPM на все времена',
        'description_ru': u'Спіс чальцоў журы CPM на зсе часы',
    }


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


def add_jury_member_pages(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')
    jury_member_page_ct = get_content_type(apps, 'results', 'jurymemberpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    homepage = HomePage.objects.get(slug='home')
    juryindex_page = add_subpage(
        parent=homepage,
        model=IndexPage,
        content_type=index_page_ct,
        **_get_juryindex_kw()
    )

    for item in _get_data():
        photo = Image(title=item['title'], collection=collection_id)
        with open(_get_photo_path(item['photo']), 'rb') as photo_file:
            photo.file.save(name=item['photo'], content=File(photo_file))
            photo.save()

        add_subpage(
            parent=juryindex_page,
            model=JuryMemberPage,
            photo=photo,
            content_type=jury_member_page_ct,
            **_get_jurymember_kw(item)
        )


def remove_jury_member_pages(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    Image = get_image_model(apps)
    Collection = apps.get_model('wagtailcore.Collection')
    IndexPage = apps.get_model('cpm_generic.IndexPage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')
    jury_member_page_ct = get_content_type(apps, 'results', 'jurymemberpage')
    collection_id = Collection.objects.filter(depth=1)[0]

    homepage = HomePage.objects.get(slug='home')
    juryindex_page = IndexPage.objects.get(slug=_get_juryindex_kw()['slug'])

    for item in _get_data():
        photo = Image.objects.get(title=item['title'],
                                  collection=collection_id)
        photo.delete()

        remove_subpage(
            parent=juryindex_page,
            model=JuryMemberPage,
            content_type=jury_member_page_ct,
            **_get_jurymember_kw(item)
        )

    remove_subpage(
        parent=homepage,
        model=IndexPage,
        content_type=index_page_ct,
        **_get_juryindex_kw()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_filmpage'),
        ('home', '0002_create_homepage'),
        ('cpm_generic', '0001_initial'),
        ('wagtailimages', '0011_image_collection'),
    ]

    operations = [
        migrations.RunPython(add_jury_member_pages, remove_jury_member_pages),
    ]
