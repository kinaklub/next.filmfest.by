# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-28 22:00
from __future__ import unicode_literals

from django.db import migrations

from cpm_generic.migration_utils import (add_subpage, remove_subpage,
                                         get_content_type)


def _add_news_index_page(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    NewsIndexPage = apps.get_model('news.NewsIndexPage')

    news_index_page_ct = get_content_type(apps, 'news', 'newsindexpage')

    homepage = HomePage.objects.get(slug='home')
    add_subpage(
        homepage,
        NewsIndexPage,
        content_type=news_index_page_ct,
        title=u'News',
        seo_title=u'News',
        show_in_menus=True,
        slug='news',
        search_description=u'News Index Page to show list of separate news articles about Cinema Perpetuum Mobile'
    )


def remove_news_index_page(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    NewsIndexPage = apps.get_model('news.NewsIndexPage')

    news_index_page_ct = get_content_type(apps, 'news', 'newsindexpage')

    homepage = HomePage.objects.get(slug='home')

    remove_subpage(
        homepage,
        NewsIndexPage,
        content_type=news_index_page_ct,
        slug='news',
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_add_news_index_page, remove_news_index_page),
    ]
