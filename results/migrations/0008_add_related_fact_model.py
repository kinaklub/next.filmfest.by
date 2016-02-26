# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_auto_20151206_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsFact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),  # noqa
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),  # noqa
                ('number', models.CharField(default='', max_length=10)),
                ('caption_en', models.CharField(default='', max_length=100)),
                ('position_en', models.CharField(default='b', max_length=1, choices=[('t', 'Top'), ('b', 'Bottom')])),  # noqa
                ('caption_be', models.CharField(default='', max_length=100)),
                ('position_be', models.CharField(default='b', max_length=1, choices=[('t', 'Top'), ('b', 'Bottom')])),  # noqa
                ('caption_ru', models.CharField(default='', max_length=100)),
                ('position_ru', models.CharField(default='b', max_length=1, choices=[('t', 'Top'), ('b', 'Bottom')])),  # noqa
                ('page', modelcluster.fields.ParentalKey(related_name='fact', to='results.ResultsPage')),  # noqa
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
