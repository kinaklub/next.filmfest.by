# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0011_add_category_to_results_jury'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsRelatedWinner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),  # noqa
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),  # noqa
                ('nomination_en', models.CharField(default='', max_length=250, blank=True)),  # noqa
                ('nomination_be', models.CharField(default='', max_length=250, blank=True)),  # noqa
                ('nomination_ru', models.CharField(default='', max_length=250, blank=True)),  # noqa
                ('film', models.ForeignKey(related_name='+', blank=True, to='results.FilmPage', null=True)),  # noqa
                ('page', modelcluster.fields.ParentalKey(related_name='related_winners', to='results.ResultsPage')),  # noqa
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
