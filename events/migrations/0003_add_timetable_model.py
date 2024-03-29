# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-27 20:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('events', '0002_venue'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),  # noqa: E501
                ('caption_en', models.CharField(max_length=1000)),
                ('caption_be', models.CharField(max_length=1000)),
                ('caption_ru', models.CharField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TimeTableEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa: E501
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),  # noqa: E501
                ('starts_at', models.DateTimeField(db_index=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_events', to='events.TimeTable')),  # noqa: E501
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='events.FilmProgram')),  # noqa: E501
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='events.Venue')),  # noqa: E501
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='event',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='event',
            name='program',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
