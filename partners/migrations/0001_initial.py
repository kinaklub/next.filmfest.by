# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-13 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('cpm_data', '0011_add_jury_data_to_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnersPage',
            fields=[
                ('page_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=models.PROTECT,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='wagtailcore.Page')
                 ),
                ('name_en', models.CharField(max_length=1000)),
                ('name_be', models.CharField(max_length=1000)),
                ('name_ru', models.CharField(max_length=1000)),
                ('entry_en', wagtail.wagtailcore.fields.RichTextField(default='')),
                ('entry_be', wagtail.wagtailcore.fields.RichTextField(default='')),
                ('entry_ru', wagtail.wagtailcore.fields.RichTextField(default='')),
                ('season', models.ForeignKey(
                    on_delete=models.PROTECT, 
                    related_name='+',
                    to='cpm_data.Season')
                 ),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
