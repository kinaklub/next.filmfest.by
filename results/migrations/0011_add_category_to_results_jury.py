# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_add_partner_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultsrelatedjurymember',
            name='category_be',
            field=models.CharField(default='', max_length=250, blank=True),
        ),
        migrations.AddField(
            model_name='resultsrelatedjurymember',
            name='category_en',
            field=models.CharField(default='', max_length=250, blank=True),
        ),
        migrations.AddField(
            model_name='resultsrelatedjurymember',
            name='category_ru',
            field=models.CharField(default='', max_length=250, blank=True),
        ),
    ]
