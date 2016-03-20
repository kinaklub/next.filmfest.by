# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('results', '0009_add_facts_12_13_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),  # noqa
                ('name_en', models.CharField(max_length=250)),
                ('name_be', models.CharField(max_length=250)),
                ('name_ru', models.CharField(max_length=250)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),  # noqa
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
