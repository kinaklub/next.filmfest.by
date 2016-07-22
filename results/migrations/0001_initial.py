# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='JuryMemberPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),  # noqa
                ('name_en', models.CharField(max_length=250)),
                ('name_be', models.CharField(max_length=250)),
                ('name_ru', models.CharField(max_length=250)),
                ('info_en', models.CharField(max_length=1000)),
                ('info_be', models.CharField(max_length=1000)),
                ('info_ru', models.CharField(max_length=1000)),
                ('photo', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),  # noqa
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
